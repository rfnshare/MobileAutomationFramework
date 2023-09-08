import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from utils.config import getConfig, setup_config

appium_driver = None


# Simulating a scenario where the Appium driver is not initialized
class AppiumDriverNotInitializedError(Exception):
    def __init__(self, message="Appium driver is not initialized"):
        super().__init__(message)


def set_and_get_config_data():
    setup_config()
    config = getConfig()
    # Get the 'udid' value from the 'AndroidAppConfig' section
    try:
        udid_string = config.get("AndroidAppConfig", "udid")
    except config.NoOptionError:
        print("No 'udid' key found in the INI file.")
        exit()
    # Split the 'udid' string by commas
    udid_list = [udid.strip() for udid in udid_string.split(",")]
    if not udid_list:
        print("No UDIDs found in the 'udid' list.")
        exit()

    # Always choose the first UDID from the list
    first_udid = udid_list[0]
    apk_file_path = config.get("AndroidAppConfig", "apkPath")
    package_name = config.get("AndroidAppConfig", "appPackage")
    launcher_activity = config.get("AndroidAppConfig", "appActivity")
    wait = config.get("AndroidAppConfig", "element_wait")
    return {
        "udid": first_udid,
        "apkPath": str(apk_file_path),
        "appPackage": str(package_name),
        "appActivity": str(launcher_activity),
        "wait": str(wait),
    }


@pytest.fixture(scope="function")
def setup(request):
    global appium_driver
    options = UiAutomator2Options()
    data = set_and_get_config_data()
    options.app = data["apkPath"]
    options.app_package = data["appPackage"]
    options.app_activity = data["appActivity"]
    options.auto_grant_permissions = True
    # chrome_driver = config.get('AndroidAppConfig', 'chromedriver')
    # options.chromedriver_executable_dir = f'{chrome_driver}'
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.implicitly_wait(int(data["wait"]))
    request.cls.driver = driver
    yield
    driver.quit()
