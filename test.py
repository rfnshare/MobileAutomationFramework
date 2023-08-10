from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import unittest
from main import BaseTest


class AppiumBasics(BaseTest):
    def test_WiFiSettingsName(self):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
        sleep(5)


if __name__ == '__main__':
    unittest.main()
