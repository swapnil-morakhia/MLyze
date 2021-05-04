from GoogleImageScrapper import GoogleImageScraper
import cv2
import face_recognition
import os

class ImageAnalysis:
    def __init__(self, person_object_name, file_name):
        self.scrape_images(person_object_name)
        self.dictionary_response = self.verify_person_object(file_name=file_name)
        self.file_name = file_name

    def scrape_images(self, person_object_name):
        webdriver_path = '.\\web_driver\\chromedriver.exe'
        image_path = '.\\static\\gallery\\downloads'

        search_keys = [person_object_name]

        # Parameters
        number_of_images = 5
        headless = False
        min_resolution = (0, 0)
        max_resolution = (5000, 5000)

        for search_key in search_keys:
            image_scrapper = GoogleImageScraper(webdriver_path, image_path, search_key, number_of_images, headless, min_resolution, max_resolution)
            image_urls = image_scrapper.find_image_urls()
            image_scrapper.save_images(image_urls)

    def verify_person_object(self, file_name):
        train_encodings = list()

        for root, dirs, files in os.walk('.\\static\\gallery\\downloads', topdown=False):
            for name in files:
                train_image = face_recognition.load_image_file(os.path.join(root, name))
                train_image = cv2.cvtColor(train_image, cv2.COLOR_BGR2RGB)

                if len(face_recognition.face_encodings(train_image)) > 0:
                    train_image_encoding = face_recognition.face_encodings(train_image)[0]
                    train_encodings.append(train_image_encoding)
        
        test_image = face_recognition.load_image_file( '.\\static\\gallery\\uploads\\' + file_name)
        print("file name in verify person object is "+ file_name)
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

        present = False
        confidence = 0

        if len(face_recognition.face_encodings(test_image)) > 0:
            test_image_encoding = face_recognition.face_encodings(test_image)[0]
            result = face_recognition.compare_faces(train_encodings, test_image_encoding)
            confidence = self.count_true(result) / len(result)
            
            present = True if confidence > 0.5 else False

        return {'present': present, 'confidence': confidence}

    def count_true(self, result):
        count = 0

        for element in result:
            if element:
                count += 1

        return count

    def analyse(self):
        return self.dictionary_response
