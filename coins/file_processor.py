
import os
import cv2
import numpy as np
from joblib import load
from django.core.files.uploadedfile import InMemoryUploadedFile

class Image(object):

    def __init__(self,
                 path_to_image: str = "",
                 inmemory_image: InMemoryUploadedFile = None,
                 name: str = ""):

        assert isinstance(path_to_image, str)
        assert isinstance(name, str)
        # Читаем изображение
        if inmemory_image:
            self._file_name = inmemory_image.name
            nparr = np.fromstring(inmemory_image.read(), np.uint8)
            self._image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif path_to_image != "":
            self._image = cv2.imread(path_to_image)
            self._file_name = name
        else:
            raise AttributeError
        self._name = name
        self._gray_image = self._get_gray_image(self._image)

    @property
    def file_name(self):
        return self._file_name

    @property
    def image(self):
        return self._image

    @property
    def gray_image(self):
        return self._gray_image

    def resize_image(self) -> None:
        d = 1024 / self._image.shape[1]
        dim = (1024, int(self._image.shape[0] * d))
        self._image = cv2.resize(
            self._image, dim, interpolation=cv2.INTER_AREA)

    def _get_gray_image(self, img: image):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), 0)

        return gray

    def get_image_properties(self):
        height, width, channels = self._image.shape
        return {"height": height, "width": width}

    def find_circles(self):
        return cv2.HoughCircles(
            self.gray_image, cv2.HOUGH_GRADIENT, 2, 30)

    def get_average_color(self):
        return [
            int(self.image[:, :, i].mean()) for i in range(self.image.shape[-1])
        ][::-1]

class CoinsDetector(object):

    def __init__(
        self, img: Image,
        coins: tuple = ({"name": "1 рубль", "value": 1},
                        {"name": "10 рублей", "value": 10},
                        {"name": "2 рубля", "value": 2},
                        {"name": "5 рублей", "value": 5})
    ):
        self._image = img
        self._coins = coins
        self._clf = self._load_model()

        self.output = self._image.image.copy()

    @property
    def image(self):
        return self._image

    @property
    def clf(self):
        return self._clf

    @property
    def coins(self):
        return self._coins

    def _load_model(self):
        full_path = os.getcwd() + "/coins/predict_models/modelCoins.joblib"
        return load(full_path)

    def predictMaterial(self, roi):
        hist = self.calcHistogram(roi)
        s = self.clf.predict([hist])
        return self.coins[int(s)]

    def calcHistogram(self, img):
        m = np.zeros(img.shape[:2], dtype="uint8")
        (w, h) = (int(img.shape[1] / 2), int(img.shape[0] / 2))
        cv2.circle(m, (w, h), 60, 255, -1)

        h = cv2.calcHist(
            [img], [0, 1, 2], m, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        return cv2.normalize(h, h).flatten()

    def get_coins_parameters(self, circles: list) -> dict:

        count = 0
        diameter = []
        located_coins = []
        coordinates = []

        for (x, y, r) in circles[0, :]:
            diameter.append(r)

        circles = np.round(circles[0, :]).astype("int")

        for (x, y, d) in circles:
            count += 1

            coordinates.append((x, y))

            roi = self.image.image[y - d:y + d, x - d:x + d]

            coin = self.predictMaterial(roi)
            located_coins.append(coin)

        return located_coins


def processFiles(files: list) -> dict:
    assert isinstance(files, list)

    images_parameters = []
    all_circles = 0
    for file in files:
        img = Image(inmemory_image=file)
        coin_detector = CoinsDetector(img)
        circles = coin_detector.image.find_circles()
        coins = coin_detector.get_coins_parameters(circles)
        count = 0
        for coin in coins:
            count += coin["value"]

        filename = img.file_name
        height = img.get_image_properties()["height"]
        width = img.get_image_properties()["width"]
        average_color = img.get_average_color()
        count_circles = len(coins)

        all_circles += count_circles

        images_parameters.append({"name": filename,
                                  "height": height,
                                  "width": width,
                                  "circles": count_circles,
                                  "average_color": average_color,
                                  "total_rubles": count})
        main_dict = {}
        main_dict["images"] = images_parameters
        main_dict["all_coins"] = all_circles

    assert isinstance(main_dict, dict)
    return main_dict
