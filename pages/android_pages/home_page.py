import datetime
import inspect
import time
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.locators.android_locators import *
from utils.common import get_logger
from utils.data import TestData


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.home_locator = HomePageLocator
        self.login_locator = LoginPageLocator
        self.common_locator = CommonLocator

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
        file_name = Path(caller_frame.f_globals["__file__"]).name

        # Get the folder name of the calling script
        script_path = Path(caller_frame.f_globals["__file__"])
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
        scroll_expression = (
            f"new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView("
            f'new UiSelector().text("{txt}"))'
        )
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
        tests = [
            driver.find_element(AppiumBy.ID, self.home_locator.logo),
            driver.find_element(AppiumBy.ID, self.home_locator.balance),
        ]
        return all(tests)

    def filling_form(self):
        driver = self.driver
        log = get_logger()
        driver.find_element(*self.login_locator.COUNTRY_DROPDOWN).click()
        self.scroll_to_text(TestData.COUNTRY)
        driver.find_element(*self.login_locator.COUNTRY).click()
        driver.find_element(*self.login_locator.NAME_FIELD).send_keys(TestData.NAME)
        driver.hide_keyboard()
        driver.find_element(*self.login_locator.GENDER).click()
        driver.find_element(*self.login_locator.LETS_SHOP).click()
        log.info("Successfully Filled The Form & Proceed To Shopping")

    def validating_blank_name_error_message(self):
        driver = self.driver
        log = get_logger()
        driver.find_element(*self.login_locator.COUNTRY_DROPDOWN).click()
        self.scroll_to_text(TestData.COUNTRY)
        driver.find_element(*self.login_locator.COUNTRY).click()
        driver.find_element(*self.login_locator.GENDER).click()
        driver.find_element(*self.login_locator.LETS_SHOP).click()
        err_msg = driver.find_element(*self.common_locator.TOAST_MESSAGE).text
        assert TestData.ERR_MSG in err_msg
        log.info(f"Successfully Validated, {err_msg}")

    def shopping(self):
        log = get_logger()
        self.filling_form()
        self.scroll_to_text(TestData.PRODUCT_ONE)
        # products = self.driver.find_elements(
        #     by=By.ID, value="com.androidsample.generalstore:id/productName"
        # )
        # for i in range(0, len(products)):
        #     print("->", products[i].text)
        #     if products[i].text == TestData.PRODUCT_ONE:
        #         (
        #             self.driver.find_elements(
        #                 by=By.ID,
        #                 value="com.androidsample.generalstore:id/productAddCart",
        #             )
        #         )[i].click()
        self.driver.find_element(By.XPATH, self.home_locator.product_add_to_cart(TestData.PRODUCT_ONE)).click()
        self.driver.find_element(*self.home_locator.CART_BUTTON).click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element(self.home_locator.CART_TITLE, "Cart"))

        # validating product name
        product_name = self.driver.find_element(*self.home_locator.PRODUCT_NAME).text
        assert TestData.PRODUCT_ONE in product_name

        # validating product price
        product_price = self.driver.find_element(*self.home_locator.TOTAL_AMOUNT).text
        assert TestData.PRODUCT_ONE_PRICE in product_price
        log.info(f"Successfully Added Product, {product_name}, Price: {product_price}")

    def validating_cart_price(self):
        log = get_logger()
        self.filling_form()
        self.scroll_to_text(TestData.PRODUCT_ONE)
        self.driver.find_element(By.XPATH, self.home_locator.product_add_to_cart(TestData.PRODUCT_ONE)).click()
        self.scroll_to_text(TestData.PRODUCT_TWO)
        self.driver.find_element(By.XPATH, self.home_locator.product_add_to_cart(TestData.PRODUCT_TWO)).click()
        log.info(
            f"Successfully Added Product, {TestData.PRODUCT_ONE} & {TestData.PRODUCT_TWO} into Cart"
        )
        self.capture_screenshot()
        self.driver.find_element(*self.home_locator.CART_BUTTON).click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element(self.home_locator.CART_TITLE, "Cart"))
        prices = self.driver.find_elements(*self.home_locator.PRODUCT_PRICE)
        count = 0
        for price in prices:
            clean_price = self.clear_amount(price.text)
            count += clean_price
        log.info(f"Total Counted Price is {count}")

        # validating product price
        total_price = self.driver.find_element(*self.home_locator.TOTAL_AMOUNT).text
        assert count == self.clear_amount(total_price)
        log.info(f"Validated Total Price: {total_price} with count: {count}")
        self.capture_screenshot()

        terms_and_conditions = self.driver.find_element(*self.home_locator.TERMS_AND_CONDITIONS_BUTTON)
        self.driver.execute_script(
            "mobile: longClickGesture",
            {"elementId": terms_and_conditions, "duration": 2000},
        )
        alert_title = self.driver.find_element(*self.home_locator.TERMS_AND_CONDITIONS_BUTTON_TITLE).text
        assert TestData.TOC_TITLE == alert_title
        log.info(f"Validated Terms Of Conditions, {alert_title}")
        self.capture_screenshot()

        self.driver.find_element(*self.common_locator.OK).click()
        self.driver.find_element(*self.home_locator.CHECKBOX).click()
        self.driver.find_element(*self.home_locator.PROCEED_BUTTON).click()

        # Switching To Webview
        web_view = (By.ID, "com.androidsample.generalstore:id/webView")
        wait.until(EC.presence_of_element_located(web_view))
        # print(self.driver.find_element(*web_view).is_displayed())
        # assert self.driver.find_element(*web_view).is_displayed()
        # Python
        time.sleep(5)
        webview = self.driver.contexts[1]
        self.driver.switch_to.context(webview)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@name='q']").send_keys(
            "Hello Appium !!!"
        )
        self.driver.find_element(By.XPATH, "//*[@name='q']").send_keys(Keys.ENTER)
        log.info(f"Validated Apps Webview")
        self.capture_screenshot()

        # Switching Back To App
        self.driver.press_keycode(4)
        self.driver.switch_to.context("NATIVE_APP")
        self.driver.find_element(*self.login_locator.GENDER).click()
        log.info(f"Validated Apps Native Interaction")
        self.capture_screenshot()
