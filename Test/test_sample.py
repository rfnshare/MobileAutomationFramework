import time
from time import sleep
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup")
class TestHomePage:
    def scroll_to_text(self, txt):
        scroll_expression = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(' \
                            f'new UiSelector().text("{txt}"))'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_expression)
    def test_fill_form(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/spinnerCountry').click()
        self.scroll_to_text("Bangladesh")
        driver.find_element(by=By.XPATH, value="//android.widget.TextView[@text='Bangladesh']").click()
        driver.find_element(by=By.ID, value="com.androidsample.generalstore:id/nameField").send_keys("Faroque")
        driver.hide_keyboard()
        driver.find_element(by=By.XPATH, value="//android.widget.RadioButton[@resource-id='com.androidsample.generalstore:id/radioFemale']").click()
        driver.find_element(by=By.ID, value='com.androidsample.generalstore:id/btnLetsShop').click()
        time.sleep(5)
