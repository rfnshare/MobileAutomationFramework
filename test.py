from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import unittest

from selenium.webdriver.common.by import By

from main import BaseTest


class AppiumBasics(BaseTest):
    def test_WiFiSettingsName(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
        self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@content-desc="3. Preference '
                                                          'dependencies"]').click()
        self.driver.find_element(by=By.ID, value='android:id/checkbox').click()
        self.driver.find_element(by=By.XPATH, value='(//android.widget.RelativeLayout)[2]').click()
        self.driver.find_element(by=By.ID, value='android:id/edit').send_keys("Testing")
        ((self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.Button'))[1]).click()

        sleep(5)


if __name__ == '__main__':
    unittest.main()
