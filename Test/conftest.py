from pathlib import Path
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService


@pytest.fixture(scope="function")
def setup(request):
    # service = AppiumService()
    options = UiAutomator2Options()
    # service.start()
    # options.avd = "Pixel_3a_API_34_extension_level_7_x86_64"
    options.udid = '54da5eee'
    options.app = f'{Path(__file__).parent.parent / "app/General-Store.apk"}'
    options.auto_grant_permissions = True
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    request.cls.driver = driver
    yield
    driver.quit()
    # service.stop()
