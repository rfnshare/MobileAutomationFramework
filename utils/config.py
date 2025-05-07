import configparser
import os
import subprocess
from pathlib import Path
import socket
import mysql.connector
from androguard.core.apk import APK
from mysql.connector import Error


def getConfig():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / "config/properties.ini")
    return config


def get_connected_device_udid():
    try:
        # Run the 'adb devices' command to list connected devices
        result = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, check=True
        )

        # Parse the output to extract the UDID of the connected device
        lines = result.stdout.strip().split("\n")[1:]  # Skip the header line
        devices = [line.split("\t")[0] for line in lines if line.strip()]

        if not devices:
            print("No connected devices found.")
            return None

        if len(devices) == 1:
            udid = devices[0]
        else:
            udid = ", ".join(devices)

        return udid
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def setup_config():
    config = getConfig()
    ini_file_path = Path(__file__).parent.parent / "config/properties.ini"
    try:
        config.read(ini_file_path)
    except FileNotFoundError:
        print(f"INI file '{ini_file_path}' not found.")
        return

    # # Get the 'apk' value from the 'AndroidAppConfig' section
    # try:
    #     apk_file_name = config.get("AndroidAppConfig", "apk")
    #     # Check if the 'apk' value is empty
    #     if not apk_file_name:
    #         print("The 'apk' key in the INI file is empty.")
    #         return
    # except config.NoOptionError:
    #     print("No 'apk' key found in the INI file.")
    #     return

    # Find APK files in the app/android folder
    apk_folder = Path(__file__).parent.parent / "app/android"
    apk_files = [file for file in os.listdir(apk_folder) if file.endswith(".apk")]

    if not apk_files:
        print("No APK files found in the app/android folder.")
        exit()
    if len(apk_files) == 1:
        apks = apk_files[0]
    else:
        print(
            "Found multiple APK files in the app/android folder. Please provide only one APK."
        )
        exit()
    # Construct the full path to the APK file
    apk_file_path = Path(__file__).parent.parent / "app/android" / apks

    # Check if the APK file exists
    if not apk_file_path.exists():
        print(f"APK file '{apk_file_path}' not found.")
        return

    # Load the APK file
    apk = APK(apk_file_path)

    # Get the package name and launcher activity
    package_name = apk.get_package()
    launcher_activity = apk.get_main_activity()

    # Call the function to get the connected device's UDID
    connected_device_udid = get_connected_device_udid()

    # Update the INI file with the extracted values
    config["AndroidAppConfig"]["apk"] = str(apks)
    config["AndroidAppConfig"]["apkPath"] = str(apk_file_path)
    config["AndroidAppConfig"]["udid"] = str(connected_device_udid)
    config["AndroidAppConfig"]["appPackage"] = str(package_name)
    config["AndroidAppConfig"]["appActivity"] = str(launcher_activity)

    # Save the changes back to the INI file
    with open(ini_file_path, "w") as configfile:
        config.write(configfile)


# will database setup later

# host, db, user, password
connect_config = {
    "user": getConfig()["SQL"]["user"],
    "password": getConfig()["SQL"]["password"],
    "host": getConfig()["SQL"]["host"],
    "database": getConfig()["SQL"]["database"],
}


def getConnection():
    try:
        conn = mysql.connector.connect(**connect_config)
        if conn.is_connected():
            print("Connected")
            return conn
    except Error as e:
        print("Error->", e)


def getQuery(query):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return row


def set_and_get_config_data():
    setup_config()
    config = getConfig()

    # Check if the APK exists in the app/android folder
    apk_folder = os.path.join(os.getcwd(), "app", "android")
    apk_file_name = config.get("AndroidAppConfig", "apkPath")

    apk_file_path = None
    if os.path.exists(os.path.join(apk_folder, apk_file_name)):
        apk_file_path = os.path.join(apk_folder, apk_file_name)

    # If the APK file path is not found, raise an error
    if apk_file_path is None:
        print("APK file not found in the app/android folder.")
        exit()

    # Get the 'udid' value from the 'AndroidAppConfig' section
    try:
        udid_string = config.get("AndroidAppConfig", "udid")
    except configparser.NoOptionError:
        print("No 'udid' key found in the INI file.")
        exit()

    # Split the 'udid' string by commas
    udid_list = [udid.strip() for udid in udid_string.split(",")]

    if not udid_list:
        print("No UDIDs found in the 'udid' list.")
        exit()

    # Get the APK name from the 'AndroidAppConfig' section
    try:
        package_name = config.get("AndroidAppConfig", "appPackage")
        launcher_activity = config.get("AndroidAppConfig", "appActivity")
        wait = config.get("AndroidAppConfig", "element_wait")
    except configparser.NoOptionError:
        print(
            "APK name or other required values not found in the 'AndroidAppConfig' section."
        )
        print(
            "Please define 'apkPath', 'appPackage', 'appActivity', and 'element_wait' in the configuration file."
        )
        exit()

    # Always choose the first UDID from the list
    first_udid = udid_list[0]

    return {
        "udid": first_udid,
        "apkPath": str(apk_file_path),
        "appPackage": str(package_name),
        "appActivity": str(launcher_activity),
        "wait": str(wait),
    }


def free_port(start_port=4723):
    """
    Determines a free port using sockets, starting from the specified start_port.
    """
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as free_socket:
            try:
                free_socket.bind(("0.0.0.0", port))
                free_socket.listen(5)
                port = free_socket.getsockname()[1]
                return port
            except OSError:
                port += 1
