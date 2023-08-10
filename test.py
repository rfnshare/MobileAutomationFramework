from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
import subprocess

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from main import BaseTest


class AppiumBasics(BaseTest):
    def WiFiSettingsName(self):
        self.ConfigureAppium()
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
        sleep(5)
        self.tearDown()


obj = AppiumBasics()
obj.WiFiSettingsName()
