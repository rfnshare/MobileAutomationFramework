from pathlib import Path

import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import datetime

from appium.webdriver.appium_service import AppiumService

from utils.config import getConfig, setup_config

driver = None


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
    global driver
    options = UiAutomator2Options()
    service = AppiumService()
    service.start()
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
    service.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    # Generate a timestamp in the format YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Start performance recording with the "Page.load" category

            file_name = (report.nodeid.replace("::", "_")).replace(
                "/", "_"
            ) + f"_{timestamp}.png"
            SS_PATH = Path(__file__).parent.parent / "reports/screenshots/failed"
            _capture_screenshot(SS_PATH / file_name)
            if file_name:
                image_path = (
                    Path(__file__).parent.parent
                    / "reports/screenshots/failed"
                    / file_name
                )
                try:
                    if driver is None:
                        raise AppiumDriverNotInitializedError
                    allure.attach(driver.get_screenshot_as_png())
                except AppiumDriverNotInitializedError as e:
                    print(f"An error occurred: {e}")

                # Encode the path to HTML-safe format
                encoded_path = image_path.as_uri()
                html = (
                    f'<div><img src="{encoded_path}" alt="screenshot" style="width:150px;height:300px;" '
                    'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))
        report.extras = extra


def _capture_screenshot(name):
    try:
        if driver is None:
            raise AppiumDriverNotInitializedError
        driver.get_screenshot_as_file(name)
    except AppiumDriverNotInitializedError as e:
        print(f"An error occurred: {e}")


def pytest_exception_interact(node, call, report):
    """
    Pending Implementation: Setup API response (request & response) data in Log
    """
    if report.failed:
        test_name = node.name  # Get the name of the test
        test_file = node.parent.nodeid  # Get the test file path

        exception_info = call.excinfo  # Get the ExceptionInfo instance
        exception_type = exception_info.type
        exception_value = exception_info.value

        print(f"Test Name: {test_name}")
        print(f"Test File: {test_file}")
        print(f"Exception Type: {exception_type}")
        print(f"Exception Value: {exception_value}")

        # pending

        # Retrieve network logs using the Appium driver
        # network_logs = driver.get_log("performance")
        # for entry in network_logs:
        #     if "Network.requestWillBeSent" in entry["message"]["method"]:
        #         request_data = entry["message"]["params"]["request"]
        #         response_data = entry["message"]["params"]["response"]
        #
        #         # Process and log network request and response data
        #         print("Request:")
        #         print(request_data)
        #         print("Response:")
        #         print(response_data)
