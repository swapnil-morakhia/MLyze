from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from PIL import Image
import requests

class GoogleImageScraper:
    def __init__(self, webdriver_path, image_path, search_key="cat", number_of_images=1, headless=False, min_resolution=(0, 0), max_resolution=(1920, 1080)):
        # Check parameter types.
        if type(number_of_images) != int:
            return

        if not os.path.exists(image_path):
            os.makedirs(image_path)

        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947" % search_key
        self.headless = headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.saved_extension = "jpg"
        self.valid_extensions = ["jpg", "png", "jpeg"]

    def find_image_urls(self):
        image_urls = []
        count = 0
        missed_count = 0
        options= webdriver.ChromeOptions()
        
        options = Options()
        options.add_argument('headless')
        
        try:
            driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
            # driver.set_window_size(1400, 1050)
            driver.minimize_window
            driver.get(self.url)
        except Exception:
            pass

        for indx in range(1, self.number_of_images + 1):
            try:
                # find and click image
                imgurl = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(indx)))
                imgurl.click()
                missed_count = 0
            except Exception:
                missed_count = missed_count + 1
                if missed_count > 10:
                    break
                else:
                    continue

            try:
                # select image from the popup
                class_names = ["n3VNCb"]
                images = [driver.find_elements_by_class_name(class_name) for class_name in class_names if
                          len(driver.find_elements_by_class_name(class_name)) != 0][0]
                for image in images:
                    # only downloads images that starts with http
                    if image.get_attribute("src")[:4].lower() in ["http"]:
                        image_urls.append(image.get_attribute("src"))
                        count += 1
                        break
            except Exception:
                pass

            try:
                # scroll page to load next image
                driver.execute_script("window.scrollTo(0, " + str(indx * 100) + ");")
                element = driver.find_element_by_class_name("mye4qd")
                element.click()
            except Exception:
                pass

        driver.close()
        return image_urls

    def save_images(self, image_urls):
        for indx, image_url in enumerate(image_urls):
            try:
                filename = "%s%s.%s" % (self.search_key, str(indx), self.saved_extension)
                image_path = os.path.join(self.image_path, filename)
                image = requests.get(image_url)
                if image.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(image.content)
                        f.close()
                        image_from_web = Image.open(image_path)
                        image_resolution = image_from_web.size

                        if image_resolution is not None:
                            if image_resolution[0] < self.min_resolution[0] or image_resolution[1] < \
                                    self.min_resolution[1] or image_resolution[0] > self.max_resolution[0] or \
                                    image_resolution[1] > self.max_resolution[1]:
                                image_from_web.close()
                                os.remove(image_path)
                        image_from_web.close()
            except Exception as e:
                pass
