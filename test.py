from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from main import BaseTest


class AppiumBasics(BaseTest):
    def test_WiFiSettingsName(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Preference').click()
        self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@content-desc="3. Preference '
                                                    'dependencies"]').click()
        self.driver.find_element(by=By.ID, value='android:id/checkbox').click()
        self.driver.find_element(by=By.XPATH, value='(//android.widget.RelativeLayout)[2]').click()
        title = self.driver.find_element(by=By.ID, value='android:id/alertTitle').text
        assert "WiFi settings" in title
        self.assertEqual(title, "WiFi settings")

        self.driver.find_element(by=By.ID, value='android:id/edit').send_keys("Testing")
        ((self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.Button'))[1]).click()

        sleep(5)

    def test_LongPress(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Views').click()
        driver.find_element(by=By.XPATH, value='//android.widget.TextView[@content-desc="Expandable Lists"]').click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='1. Custom Adapter').click()
        element = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="People Names"]')
        driver.execute_script('mobile: longClickGesture', {'elementId': element, 'duration': 2000})
        title_txt = driver.find_element(by=By.ID, value='android:id/title').text
        self.assertEqual(title_txt, 'Sample menu')
        self.assertTrue(driver.find_element(by=By.ID, value='android:id/title').is_displayed())
        driver.find_element(by=By.XPATH, value="//android.widget.TextView[@text='Sample action']").click()
        toast_msg = driver.find_element(by=By.XPATH, value="//android.widget.Toast")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.Toast")))
        print(toast_msg.text)
        # self.assertEqual(toast_msg.text, 'People Names: Group 0 clicked')
        self.assertIn('Group 0 clicked', toast_msg.text)
        sleep(5)


if __name__ == '__main__':
    unittest.main()
