from pathlib import Path
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService


@pytest.fixture(scope="class")
def setup(request):
    # service = AppiumService()
    options = UiAutomator2Options()
    # service.start()
    options.avd = "Pixel_3a_API_34_extension_level_7_x86_64"
    options.app = "D:/resources/ApiDemos-debug.apk"
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    request.cls.driver = driver
    yield
    driver.quit()
    # service.stop()
