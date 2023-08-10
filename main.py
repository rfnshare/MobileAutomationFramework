from appium.options.android import UiAutomator2Options
from appium import webdriver


class BaseTest:
    def __init__(self):
        self.driver = None

    def ConfigureAppium(self):
        # service = AppiumService()
        options = UiAutomator2Options()
        # service.start()
        options.avd = "Pixel_3a_API_34_extension_level_7_x86_64"
        options.app = "D:/resources/ApiDemos-debug.apk"
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    def tearDown(self):
        self.driver.close()
