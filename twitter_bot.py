from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from dotenv import load_dotenv
import os

# Uploading env data
load_dotenv(".env")

# Setting driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.speedtest.net/")
        self.wait = WebDriverWait(self.driver, 10)
        self.speed = 0
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")

    def find_and_click(self, ec, by, value):
        """Finds and clicks an element by provided method and its value"""
        try:
            element = self.wait.until(ec.element_to_be_clickable((by, value)))
            element.click()
        except Exception as e:
            print(f"Error clicking element {value}: {e}")

    def input_data(self, ec, by, value, data, *args):
        """Finds and inputs data to an element by provided method and its value;
        possible to provide args which are keys that will be pressed after inputting data"""
        try:
            element = self.wait.until(ec.element_to_be_clickable((by, value)))
            if args:
                element.send_keys(data, *args)
            else:
                element.send_keys(data)
        except Exception as e:
            print(f"Error clicking element {value}: {e}")

    def is_numeric(self, text):
        """Checks if the text contains a numeric value (digit or floating point)"""
        return bool(re.search(r'\d', text))

    def download_speed(self, by):
        """Retrieves download speed amount and returns it as float number"""
        try:
            WebDriverWait(self.driver, 60).until(
                lambda d: self.is_numeric(d.find_element(by, "download-speed").text)
            )
            self.speed = float(self.driver.find_element(by, "download-speed").text)
            return self.speed

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def x_log_in(self):
        """Logs in to the X account"""
        self.driver.get("https://x.com/home")

        login_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/login"]')))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        login_button.click()

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class*='r-30o5oe']")))
        self.input_data(EC, By.CSS_SELECTOR, "input[class*='r-30o5oe']",
                        f"{self.email}", Keys.ENTER)

        self.input_data(EC, By.CSS_SELECTOR, "input[class*='r-1dz5y72']",
                        f"{self.password}", Keys.ENTER)

        close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                   "button[class*='css-175oi2r']")))
        close_button.click()

    def make_a_tweet(self):
        """Sends a tweet with speed value"""
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.DraftEditor-root")))
        tweet_input = self.driver.find_element(By.CSS_SELECTOR, "div.DraftEditor-root")
        tweet_input.click()
        self.input_data(EC, By.CLASS_NAME, "div.DraftEditor-root",
                        f"My internet speed is {self.speed}")
        self.find_and_click(EC, By.CSS_SELECTOR, "button[class*='css-175oi2r']")

        self.driver.quit()



