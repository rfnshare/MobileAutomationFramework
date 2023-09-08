import configparser
from pathlib import Path
import mysql.connector
from mysql.connector import Error
import subprocess
import androguard
from androguard.core.bytecodes.apk import APK

def getConfig():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / 'config/properties.ini')
    return config


def get_connected_device_udid():
    try:
        # Run the 'adb devices' command to list connected devices
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)

        # Parse the output to extract the UDID of the connected device
        lines = result.stdout.strip().split('\n')[1:]  # Skip the header line
        devices = [line.split('\t')[0] for line in lines if line.strip()]

        if not devices:
            print("No connected devices found.")
            return None

        if len(devices) == 1:
            udid = devices[0]
        else:
            udid = ', '.join(devices)

        return udid
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def setup_config():
    config = getConfig()
    ini_file_path = Path(__file__).parent.parent / 'config/properties.ini'
    try:
        config.read(ini_file_path)
    except FileNotFoundError:
        print(f"INI file '{ini_file_path}' not found.")
        return

    # Get the 'apk' value from the 'AndroidAppConfig' section
    try:
        apk_file_name = config.get('AndroidAppConfig', 'apk')
        # Check if the 'apk' value is empty
        if not apk_file_name:
            print("The 'apk' key in the INI file is empty.")
            return
    except config.NoOptionError:
        print("No 'apk' key found in the INI file.")
        return

    # Construct the full path to the APK file
    apk_file_path = Path(__file__).parent.parent / "app/android" / apk_file_name

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
    config['AndroidAppConfig']['ApkPath'] = str(apk_file_path)
    config['AndroidAppConfig']['udid'] = str(connected_device_udid)
    config['AndroidAppConfig']['apppackage'] = str(package_name)
    config['AndroidAppConfig']['appactivity'] = str(launcher_activity)

    # Save the changes back to the INI file
    with open(ini_file_path, 'w') as configfile:
        config.write(configfile)


# will database setup later

# host, db, user, password
connect_config = {
    'user': getConfig()['SQL']['user'],
    'password': getConfig()['SQL']['password'],
    'host': getConfig()['SQL']['host'],
    'database': getConfig()['SQL']['database']
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
