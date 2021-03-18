from django.test import TestCase
from .file_processor import processFiles


class FileProcessor(TestCase):

    def test_file_process(self):
        file = open("./coins/test_images/1.jpg", "rb")
        file2 = open("./coins/test_images/2.jpg", "rb")
        file_list = [file, file2]
        process_data = processFiles(file_list)
        # Первое изображение
        self.assertEqual(
            process_data["images"][0]["name"], "./coins/test_images/1.jpg")
        self.assertEqual(process_data["images"][0]["width"], 1536)
        self.assertEqual(process_data["images"][0]["height"], 2048)
        self.assertEqual(process_data["images"][0]["total_rubles"], 106)
        self.assertEqual(
            process_data["images"][0]["average_color"], [78, 116, 117])
        # Второе изображение
        self.assertEqual(
            process_data["images"][1]["name"], "./coins/test_images/2.jpg")
        self.assertEqual(process_data["images"][1]["width"], 1536)
        self.assertEqual(process_data["images"][1]["height"], 2048)
        self.assertEqual(process_data["images"][0]["total_rubles"], 106)
        self.assertEqual(
            process_data["images"][1]["average_color"], [76, 115, 116])

        self.assertEqual(process_data["all_coins"], 50)
