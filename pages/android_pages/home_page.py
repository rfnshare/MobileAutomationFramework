import time
import datetime
from pathlib import Path
from time import sleep
import inspect

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.common import get_logger
from utils.config import getConfig
from utils.data import TestData

from utils.android_locators import *


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.home_locator = HomePageLocator
        self.login_locator = LoginPageLocator
        self.log = get_logger()

    def wait(self, method, locator):
        """
            Check if all elements on the home page are visible.

            Returns:
                None
        """
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((method, locator)))

    def capture_screenshot(self):
        """
            Capture SS For Particular Page. Naming Convention generated with timestamp, folder, file, class name

            Returns:
                None
        """
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)[1][0]

        # Get test case function name and class name
        function_name = caller_frame.f_code.co_name
        class_name = self.__class__.__name__

        # Get Python file name
        file_name = Path(caller_frame.f_globals['__file__']).name

        # Get the folder name of the calling script
        script_path = Path(caller_frame.f_globals['__file__'])
        calling_folder_name = script_path.parent.name

        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")

        # Generate screenshot file name
        screenshot_name = f"{calling_folder_name}_{file_name}_{class_name}_{function_name}_{timestamp}.png"

        # Construct screenshot file path
        SS_PATH = Path(__file__).parent.parent.parent / "reports/screenshots/passed"
        screenshot_path = SS_PATH / screenshot_name

        # Take the screenshot and save it
        self.driver.get_screenshot_as_file(screenshot_path)

    def scroll_to_text(self, txt):
        """
        This method help with scroll to defined text
        :return:
        """
        scroll_expression = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(' \
                            f'new UiSelector().text("{txt}"))'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_expression)

    def clear_amount(self, price_str):
        # Remove the "$" symbol and any commas from the string
        cleaned_price_str = price_str.replace("$", "").replace(",", "")

        try:
            # Convert the cleaned string to a float
            price_float = float(cleaned_price_str)
            return price_float
        except ValueError:
            # Handle any conversion errors
            return None

    def check_home_page_elements(self):
        """
        This method checks if all the elements on the home page are visible
        :return:
        """
        driver = self.driver
        tests = [driver.find_element(AppiumBy.ID, self.home_locator.logo),
                 driver.find_element(AppiumBy.ID, self.home_locator.balance)]
        return all(tests)

    def filling_form(self):
        driver = self.driver
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/spinnerCountry').click()
        self.scroll_to_text("Bangladesh")
        driver.find_element(by=By.XPATH, value="//android.widget.TextView[@text='Bangladesh']").click()
        driver.find_element(by=By.ID, value="com.androidsample.generalstore:id/nameField").send_keys(TestData.NAME)
        driver.hide_keyboard()
        driver.find_element(by=By.XPATH,
                            value="//android.widget.RadioButton[@resource-id='com.androidsample.generalstore:id/radioFemale']").click()
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/btnLetsShop').click()
        self.log.info("Successfully Filled The Form")

    def validating_blank_name_error_message(self):
        driver = self.driver
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/spinnerCountry').click()
        self.scroll_to_text(TestData.COUNTRY)
        driver.find_element(by=By.XPATH, value="//android.widget.TextView[@text='Bangladesh']").click()
        driver.find_element(by=By.XPATH,
                            value="//android.widget.RadioButton[@resource-id='com.androidsample.generalstore:id/radioFemale']").click()
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/btnLetsShop').click()
        err_msg = driver.find_element(by=By.XPATH, value="//android.widget.Toast[1]").text
        print(err_msg)
        assert TestData.ERR_MSG in err_msg
        self.log.info(f"Successfully Validated, {err_msg}")

    def shopping(self):
        self.filling_form()
        self.scroll_to_text(TestData.PRODUCT_ONE)
        # self.driver.find_element(by=By.XPATH, value="//android.widget.TextView[@text='Jordan 6 "
        #                                             "Rings']/parent::android.widget.LinearLayout//android.widget.TextView[@text='ADD TO CART']").click()
        products = self.driver.find_elements(by=By.ID, value="com.androidsample.generalstore:id/productName")
        for i in range(0, len(products)):
            print("->", products[i].text)
            if products[i].text == TestData.PRODUCT_ONE:
                (self.driver.find_elements(by=By.ID, value="com.androidsample.generalstore:id/productAddCart"))[
                    i].click()
        self.driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/appbar_btn_cart').click()

        # validating product name
        cart = (By.XPATH, "//android.widget.TextView[@text='Cart']")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element(cart, "Cart"))
        print(self.driver.find_element(*cart).text)

        p_n = self.driver.find_element(by=By.ID, value="com.androidsample.generalstore:id/productName").text
        assert TestData.PRODUCT_ONE in p_n
        # validating product price
        p_p = self.driver.find_element(by=By.ID, value="com.androidsample.generalstore:id/totalAmountLbl").text
        print(p_p)
        assert TestData.PRODUCT_ONE_PRICE in p_p
