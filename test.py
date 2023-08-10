from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
import subprocess

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


class Setup:
    # service = AppiumService()
    options = UiAutomator2Options()

    def AppiumTest(self):
        # service.start()
        self.options.avd = "Pixel_3a_API_34_extension_level_7_x86_64"
        self.options.app = "D:/resources/ApiDemos-debug.apk"
        driver = webdriver.Remote("http://127.0.0.1:4723", options=self.options)
        return driver
        # driver.quit()


driver_obj = Setup()
driver = driver_obj.AppiumTest()
driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
sleep(5)
driver.quit()
