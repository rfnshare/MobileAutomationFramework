from time import sleep

from appium.webdriver.common.appiumby import AppiumBy

from Src.TestBase.AppiumDriverSetup import WebDriverSetup


class TestHomePage(WebDriverSetup):
    def test_one(self):
        driver = self.driver
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
        sleep(5)