import cv2
import numpy as np


def processFiles(files: list) -> dict:
    assert isinstance(files, list)

    images_parameters = []
    all_circles = 0
    for file in files:
        filename = file.name
        # Загрузка изображения
        nparr = np.fromstring(file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Высота и ширина
        height, width, channels = image.shape
        # Средний цвет
        average_color = [
            int(image[:, :, i].mean()) for i in range(image.shape[-1])]

        # Ищем монеты
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), 0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 30)

        if circles is not None:
            count_circles = len(circles[0])
        else:
            count_circles = 0
        all_circles += count_circles

        images_parameters.append({"name": filename,
                                  "height": height,
                                  "width": width,
                                  "circles": count_circles,
                                  "average_color": average_color})

        main_dict = {}
        main_dict["images"] = images_parameters
        main_dict["all_coins"] = all_circles

    assert isinstance(main_dict, dict)
    return main_dict
