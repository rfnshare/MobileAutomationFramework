import time
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from main import BaseTest


class AppiumBasics(BaseTest):
    def scroll(self, txt):
        scroll_expression = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(' \
                            f'new UiSelector().text("{txt}"))'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_expression)

    def scroll_to_end(self):
        scroll_ = True
        # Scroll Until End [Make reusable funtion also for scroll till some element for specific element]
        while scroll_ is True:
            scroll_ = self.driver.execute_script('mobile: scrollGesture', {
                'left': 100, 'top': 100, 'width': 200, 'height': 200,
                'direction': 'down',
                'percent': 3.0
            })
        print(scroll_)

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

    def test_ScrollDemo(self):
        driver = self.driver
        driver.implicitly_wait(10)
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Views').click()
        # scroll_expression = 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(' \
        #                     'new UiSelector().text("WebView"))'
        # driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_expression)
        # self.scroll("WebView")
        self.scroll_to_end()
        sleep(5)

    def test_SwipeDemo(self):
        driver = self.driver
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Views').click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Gallery').click()
        driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="1. Photos"]').click()
        print(driver.find_element(by=By.XPATH, value="(//android.widget.ImageView)[1]").get_attribute(
            "focusable"))
        assert driver.find_element(by=By.XPATH, value="(//android.widget.ImageView)[1]").get_attribute(
            "focusable") == 'true'
        e = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.ImageView)[1]')
        driver.execute_script("mobile: swipeGesture", {'elementId': e, 'direction': 'left', 'percent': 0.75})
        assert driver.find_element(by=By.XPATH, value="(//android.widget.ImageView)[1]").get_attribute(
            "focusable") == 'false'

    def test_DragAndDrop(self):
        driver = self.driver
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Views').click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Drag and Drop').click()
        src_element = driver.find_element(by=By.ID, value='io.appium.android.apis:id/drag_dot_1')
        dst_element = driver.find_element(by=By.ID, value='io.appium.android.apis:id/drag_dot_2')
        driver.execute_script("mobile: dragGesture", {"elementId": src_element, "endX": 654,
                                                      "endY": 584})
        txt = driver.find_element(by=By.ID, value='io.appium.android.apis:id/drag_result_text').text
        assert txt == 'Dropped!', f"Expected: {txt}, Actual: 'Dropped!'"
        time.sleep(5)


if __name__ == '__main__':
    unittest.main()
