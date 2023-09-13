from pathlib import Path
import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import datetime
from appium.webdriver.appium_service import AppiumService
from utils.common import check_appium, check_environment, create_json_capabilities
from utils.config import getConfig, setup_config, set_and_get_config_data, free_port

driver = None


# Simulating a scenario where the Appium driver is not initialized
class AppiumDriverNotInitializedError(Exception):
    def __init__(self, message="Appium driver is not initialized"):
        super().__init__(message)


@pytest.fixture(scope="function")
def setup(request):
    check_environment()  # Checking node js installed or not, ENV variables set or not
    global driver
    options = UiAutomator2Options()
    data = set_and_get_config_data()
    port = free_port(start_port=4723)  # Start from port 4723 and find an available port
    service = AppiumService()
    service.start(args=["--address", "localhost", "-p", str(port)])
    appium_server_url = f"http://localhost:{port}"
    print("Running on:", appium_server_url)
    options.udid = data["udid"]
    options.app = data["apkPath"]
    options.app_package = data["appPackage"]
    options.app_activity = data["appActivity"]
    options.auto_grant_permissions = True
    # chrome_driver = config.get('AndroidAppConfig', 'chromedriver')
    # options.chromedriver_executable_dir = f'{chrome_driver}'
    check_appium(appium_server_url)  # Checking Appium Server Compatible Version
    create_json_capabilities()  # create json capabilities in json format for future use. Ex: For Appium Inspector
    driver = webdriver.Remote(appium_server_url, options=options)
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
