from appium.options.android import UiAutomator2Options
from appium import webdriver
import unittest


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options()
        # options.avd = "Pixel_3a_API_34_extension_level_7_x86_64"
        options.udid = '54da5eee'
        # options.app = "D:/resources/ApiDemos-debug.apk"
        options.app_package = "io.appium.android.apis"
        options.app_activity = "io.appium.android.apis.ApiDemos"
        cls.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    @classmethod
    def tearDownClass(cls):
        if cls.driver is not None:
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
