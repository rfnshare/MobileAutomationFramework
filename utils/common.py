import glob
import inspect
import logging.config
import os
import re
from datetime import datetime
from pathlib import Path
import subprocess
import pandas as pd
import requests
import sys


def get_logger():
    config_file_path = Path(__file__).parent.parent / "config/logging.conf"
    project_path = Path(__file__).parent.parent
    # Define a custom log filename
    log_filename = project_path.as_posix() + "/" + "reports/logs/logfile.log"

    # Check if the log directory exists; if not, create it
    log_directory = os.path.dirname(log_filename)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        print(f"Log File Created in {log_directory}")

    logging.config.fileConfig(config_file_path, defaults={"log_filename": log_filename})
    # logger_name = inspect.stack()[1][3]
    # Get the caller's frame
    caller_frame = inspect.currentframe().f_back

    # Extract the caller function name
    logger_name = caller_frame.f_code.co_name
    logger = logging.getLogger(logger_name)
    return logger


def get_test_data(sheet_name):
    excel_path = Path(__file__).parent.parent / "utils/testdata.xlsx"
    df = pd.read_excel(excel_path, sheet_name=sheet_name, dtype=str)
    df_filled = df.fillna("")
    return df_filled.to_dict(orient="records")


def get_html_reports():
    reports = []
    try:
        path = Path(__file__).parent.parent / f"reports/htmlreport/regression_*.html"
        report = os.path.abspath(glob.glob(f"{path}")[-1])
        reports.append(report)
    except Exception as e:
        print("Report not ready, Error", e)
    return reports


# Read current date
def read_date():
    return str(datetime.today().strftime("%Y-%m-%d"))


def read_time():
    return str(datetime.today().strftime("%I-%M-%S-%p"))


def clean_directory(directory):
    exclude_dirs = [
        "screenshots",
        "allure_report",
        "htmlreport",
        "logs",
        "xml_report",
        "failed",
        "passed",
    ]
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file: {file_path} - {e}")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir.lower() not in exclude_dirs:
                try:
                    os.rmdir(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete folder: {dir_path} - {e}")


def get_appium_server_version(appium_server_url):
    try:
        # Send a GET request to the Appium server's status endpoint
        response = requests.get(f"{appium_server_url}/status")
        response_json = response.json()

        # Extract and return the Appium server version
        appium_server_version = response_json.get("value", {}).get("build", {}).get("version", "Version not found")
        return appium_server_version

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting Appium server version: {str(e)}")
        return None


def check_appium(server):
    try:
        # Get the Appium version
        appium_version = get_appium_server_version(server)
        print("Running Appium version:", appium_version)

        # Check Appium version and print an error message if it's 1.22 or lower
        if appium_version and tuple(map(int, re.findall(r'\d+', appium_version))) <= (1, 22, 0):
            raise EnvironmentError(
                f"Appium version {appium_version} is installed. Please upgrade to version 2.0.0 or higher.")

    except ImportError:
        raise EnvironmentError("Appium is not installed or accessible.")


def find_java_jdk_path():
    # Define the search patterns for JDK installation directories on Linux, macOS, and Windows
    linux_pattern = '/usr/lib/jvm/java-*'
    mac_pattern = '/Library/Java/JavaVirtualMachines/jdk*'
    windows_pattern = r"C:\Program Files\Java\jdk-*"

    # Determine the current operating system
    current_os = os.name

    if current_os == 'posix':  # Linux or macOS
        # Use glob to find JDK directories that match the patterns on Linux and macOS
        jdk_paths = glob.glob(linux_pattern) + glob.glob(mac_pattern)
    elif current_os == 'nt':  # Windows
        # Use glob to find JDK directories that match the pattern on Windows
        jdk_paths = glob.glob(windows_pattern)
    else:
        raise EnvironmentError("Unsupported operating system.")

    if not jdk_paths:
        raise EnvironmentError("No Java JDK installations found matching the patterns.")

    # Return the first matching JDK path (you can modify this if multiple JDKs are installed)
    return jdk_paths[0]


def find_android_sdk_path():
    # Try to find the Android SDK path based on the user's home directory
    home = str(Path.home())
    potential_sdk_paths = [
        os.path.join(home, "AppData", "Local", "Android", "Sdk"),  # Windows
        os.path.join(home, "Library", "Android", "sdk"),  # macOS
        os.path.join(home, "Android", "Sdk"),  # Linux
    ]

    for path in potential_sdk_paths:
        if os.path.exists(path):
            return path

    # If the SDK path is not found, you can raise an exception or return None
    raise EnvironmentError(
        "Android SDK path not found. Please install the Android SDK and set it up correctly."
    )


def check_environment():
    try:
        # Check if JAVA_HOME is set
        java_home = os.environ.get("JAVA_HOME")

        if not java_home:
            print("JAVA_HOME environment variable is not set. Setting it now...")
            try:
                java_jdk_path = find_java_jdk_path()
                print("Java JDK path:", java_jdk_path)
                # Set JAVA_HOME to the appropriate value
                # Replace 'your_java_home_path' with the actual path to your Java installation
                os.environ["JAVA_HOME"] = java_jdk_path
                java_home = os.environ["JAVA_HOME"]
                print("JAVA_HOME set to:", java_home)
            except EnvironmentError as e:
                print(f"Error: {e}")
        if not java_home:
            print("JAVA_HOME is still not set. Please set it manually.")
            sys.exit(1)  # Exit the program with a non-zero exit code
        print("Found JAVA_HOME:", java_home)

        # Check if Java version is accessible
        try:
            java_version_output = subprocess.check_output(
                ["java", "-version"], stderr=subprocess.STDOUT, universal_newlines=True
            )
            if not any(char.isdigit() for char in java_version_output):
                raise EnvironmentError("Java SDK is not installed or accessible.")
        except subprocess.CalledProcessError as e:
            raise EnvironmentError("Java SDK is not installed or accessible.")

        # Check if ANDROID_HOME is set
        android_home = os.environ.get("ANDROID_HOME")
        print("Found ANDROID_HOME:", android_home)
        if not android_home:
            print("ANDROID_HOME environment variable is not set. Setting it now...")
            try:
                android_sdk_path = find_android_sdk_path()
                print("Extract Android SDK path:", android_sdk_path)
                # Set ANDROID_HOME to the appropriate value
                # Replace 'your_android_home_path' with the actual path to your Android SDK installation
                os.environ["ANDROID_HOME"] = android_sdk_path
                android_home = os.environ["ANDROID_HOME"]
                print("ANDROID_HOME set to:", android_home)
            except EnvironmentError as e:
                print(f"Error: {e}")
        if not android_home:
            print("ANDROID_HOME is still not set. Please set it manually.")
            sys.exit(1)  # Exit the program with a non-zero exit code

        print("Found ANDROID_HOME:", android_home)

        # Check Android SDK paths
        android_sdk_paths = [
            os.path.join(android_home, "platform-tools"),  # Path to platform-tools
            os.path.join(android_home, "build-tools")  # Path to build-tools
            # Add more paths as needed
        ]

        for path in android_sdk_paths:
            print("Found android_sdk_paths:", path)
            if not os.path.exists(path):
                raise EnvironmentError(f"Android SDK path not found: {path}")

        # Check if Node.js is installed
        try:
            nodejs_version_output = subprocess.check_output(
                ["node", "--version"], stderr=subprocess.STDOUT, universal_newlines=True
            )
            if not re.search(r"v\d+\.\d+\.\d+", nodejs_version_output):
                raise EnvironmentError("Node.js is not installed or accessible.")
        except subprocess.CalledProcessError as e:
            raise EnvironmentError("Node.js is not installed or accessible.")

    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code
