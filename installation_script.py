import glob
import os
import platform
import re
import subprocess
import sys
import getpass
from pathlib import Path

"""
Pending Work:
- handle brew automatically [Linux, MacOs & windows] pending
- handle install java, jre, android sdk install [windows] pending
- handle node version, if old then update [For now manual install]
- brew path permanent [Solve not found for some devices]
- git install handle (optional)
- manage with multiple package manager [sudo, brew]
- java [jdk, jre], android sdk path not setting permanently [some devices]
"""


def execute_sudo_command(command):
    sudo_password = getpass.getpass("Enter your sudo password: ")
    p = os.system("echo %s|sudo -S %s" % (sudo_password, command))
    if p == 0:
        return True
    else:
        return False


def install_chocolatey():
    # PowerShell command to install Chocolatey
    powershell_command = [
        "powershell.exe",
        "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = ["
        "System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object "
        "System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    ]

    try:
        # Run the PowerShell command to install Chocolatey
        subprocess.run(powershell_command, check=True)
        print("Chocolatey has been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def check_chocolatey_installed():
    try:
        # Run the choco -v command to check if Chocolatey is installed
        result = subprocess.run(["choco", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        print("Chocolatey is not installed.")
        return None


def is_curl_installed():
    try:
        subprocess.run(
            ["curl", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_curl():
    system_platform = platform.system()

    if system_platform == "Windows":
        print(
            "You might already have curl. Curl installation on Windows is not supported via Python script. Do it "
            "manually"
        )
        return
    elif system_platform == "Darwin":  # macOS
        try:
            subprocess.run(["brew", "install", "curl"], check=True)
            print("Curl installed successfully on macOS.")
        except subprocess.CalledProcessError:
            print("Failed to install curl on macOS.")
    elif system_platform == "Linux":
        try:
            command = "apt install curl"
            execute_sudo_command(command)
            print("Curl installed successfully on Linux.")
        except subprocess.CalledProcessError:
            print("Failed to install curl on Linux.")
    else:
        print("Unsupported operating system.")


def is_homebrew_installed():
    try:
        if sys.platform == "darwin":  # macOS
            # Check if Homebrew is installed on macOS by running 'brew --version'
            subprocess.run(
                ["brew", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            print(
                "Homebrew is found. You can continue with your Homebrew-related tasks."
            )
            return True
        elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
            # Check if Homebrew is installed on Linux
            homebrew_install_path = "/home/linuxbrew/.linuxbrew/bin/brew"
            subprocess.run(
                [homebrew_install_path, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            print(
                "Homebrew is found. You can continue with your Homebrew-related tasks."
            )
            return True
        elif sys.platform == "win32":  # Windows
            # Check if Homebrew is installed on Windows
            # homebrew_install_path = r"C:\Program Files\Git\usr\bin\brew.exe"  # Update with the actual path
            # subprocess.run([homebrew_install_path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #                check=True)
            print("Brew Check Skipping For Now For Windows")
            return True
        else:
            return False  # Unsupported platform
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Home Brew Not Found, Please Follow Readme For Installation...")
        return False


def install_homebrew():
    pass  # will implement later, now install manually. Follow README_FOR_INSTALLATION.md


def is_nodejs_installed():  # need to check version also
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            node_version = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            npm_version = subprocess.run(
                ["npm", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            print(
                f"Found Nodejs {node_version.stdout.strip()} & npm {npm_version.stdout.strip()}"
            )
        else:  # Linux and macOS
            node_version = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            npm_version = subprocess.run(
                ["npm", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            print(
                f"Found Nodejs {node_version.stdout.strip()} & npm {npm_version.stdout.strip()}"
            )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"An error occurred while checking Node.js and npm")
        return False


def install_nodejs():
    system_platform = os.name

    if system_platform == "posix":  # Linux and macOS
        try:
            install_command = ["brew", "install", "nodejs"]
            subprocess.run(install_command)

        except FileNotFoundError:
            print(
                "Node.js installation failed. Please check brew or install Node.js and npm manually."
            )
            return None
    elif system_platform == "nt":  # Windows
        try:
            install_command = ["choco", "install", "nodejs", "-y"]
            subprocess.run(install_command, shell=True)

        except FileNotFoundError:
            print(
                "Node.js installation failed. Please install Node.js and npm manually."
            )
            return None
    else:
        print("Unsupported operating system")
        return

    # Verify Node.js and npm installation
    if not is_nodejs_installed():
        print("Node.js installation failed. Please install Node.js and npm manually.")
        return
    else:
        print("Node.js and npm installation successful.")


def get_appium_version():
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            result = subprocess.run(
                ["appium", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=True,
            )
        else:  # Linux and macOS
            result = subprocess.run(
                ["appium", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

        version_match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
        if version_match:
            return version_match.group(1)
        else:
            return None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def get_node_version():
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            result = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=True,
            )
        else:  # Linux and macOS
            result = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

        version_match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
        if version_match:
            return version_match.group(1)
        else:
            return None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def install_appium():
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            subprocess.run(
                ["npm", "install", "-g", "appium"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=True,
            )
            subprocess.run(["appium", "driver", "install", "uiautomator2"], shell=True)
            subprocess.run(["appium", "driver", "install", "xcuitest"], shell=True)
        else:  # Linux and macOS
            subprocess.run(
                ["npm", "install", "-g", "appium"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        subprocess.run(["appium", "driver", "install", "uiautomator2"])
        subprocess.run(["appium", "driver", "install", "xcuitest"])
        print("Successfully Installed Appium & Drivers...")
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def update_appium():
    user_response = (
        input(
            "Appium version is older than 2.0.0. Do you want to uninstall the existing Appium and install the "
            "latest version? (yes/no): "
        )
        .strip()
        .lower()
    )
    if user_response == "yes":
        system_platform = os.name
        if system_platform == "nt":  # Windows
            subprocess.run(["npm", "uninstall", "-g", "appium"], shell=True)
        else:
            subprocess.run(["npm", "uninstall", "-g", "appium"])
        print("Uninstalling the existing Appium...")
        # Reinstall Appium
        install_appium()
        print("Latest Appium Installed Successfully...")
    else:
        print("Skipping Appium installation.")
        return


def check_java():
    try:
        # Check for JDK
        java = subprocess.run(
            ["javac", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        jdk_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("JDK Not Found")
        jdk_installed = False

    try:
        # Check for JRE
        subprocess.run(
            ["java", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        jre_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("JRE Not Found")
        jre_installed = False

    return jdk_installed, jre_installed


def install_java():
    system = platform.system()

    if system == "Linux":
        # Install OpenJDK on Linux
        subprocess.run(
            ["sudo", "apt-get", "install", "openjdk-11-jdk", "openjdk-11-jre", "-y"]
        )
    elif system == "Darwin":
        # Install AdoptOpenJDK on macOS (you can adjust this based on your macOS package manager)
        subprocess.run(["brew", "install", "adoptopenjdk11"])
    elif system == "Windows":
        # You can add Windows-specific installation commands here
        try:
            install_command = ["choco", "install", "openjdk", "-y"]
            subprocess.run(install_command, shell=True)

        except FileNotFoundError:
            print(
                "JDK installation failed. Please install manually."
            )
            return None
    else:
        print("Unsupported operating system.")


def find_sdk_directory():
    system = platform.system()
    home_dir = os.path.expanduser("~")

    if system == "Linux":
        possible_paths = [
            "/usr/local/android-sdk",  # Common installation path on Linux
            f"{home_dir}/Android/Sdk",  # Android Studio default SDK path
            "/usr/lib/android-sdk",
        ]
    elif system == "Darwin":
        possible_paths = [
            "/usr/local/android-sdk",  # Common installation path on macOS
            f"{home_dir}/Library/Android/sdk",  # Android Studio default SDK path on macOS
        ]
    elif system == "Windows":
        possible_paths = [
            f"{home_dir}\\AppData\\Local\\Android\\Sdk",  # Default SDK path on Windows
            "C:\\Android\\android-sdk"
        ]
    else:
        print("Unsupported operating system.")
        return None

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def check_sdk():
    sdk_directory = find_sdk_directory()
    print(f"SDK Path: {sdk_directory}")
    return sdk_directory is not None


def install_sdk():
    system = platform.system()

    if system == "Linux":
        # Install Android SDK on Linux
        subprocess.run(["sudo", "apt-get", "install", "android-sdk", "-y"])
    elif system == "Darwin":
        # Install Android SDK on macOS (you can adjust this based on your macOS package manager)
        subprocess.run(["brew", "install", "android-sdk"])
    elif system == "Windows":
        try:
            install_command = ["choco", "install", "android-sdk", "-y"]
            subprocess.run(install_command, shell=True)

        except FileNotFoundError:
            print(
                "Android-SDK installation failed. Please install manually."
            )
            return None
        return
    else:
        print("Unsupported operating system.")


def find_java_jdk_path():
    # Define search patterns for JDK installation directories
    jdk_patterns = {
        "posix": ["/usr/lib/jvm/java-*"],
        "nt": [r"C:\Program Files\Java\jdk-*", r"C:\Program Files\OpenJDK\jdk-*"]
    }

    current_os = os.name
    jdk_paths = []

    if current_os in jdk_patterns:
        patterns = jdk_patterns[current_os]
        for pattern in patterns:
            jdk_paths += glob.glob(pattern)

    if not jdk_paths:
        raise EnvironmentError("No Java JDK installations found matching the patterns.")

    return jdk_paths[0]  # Return the first matching JDK path


def check_environment():
    try:
        # Check if JAVA_HOME is set
        java_home = os.environ.get("JAVA_HOME")

        if not java_home:
            print("JAVA_HOME environment variable is not set. Setting it now...")
            try:
                java_jdk_path = find_java_jdk_path()
                if java_jdk_path is None:
                    print("JAVA Path Not Found....")
                    return
                os.environ["JAVA_HOME"] = java_jdk_path
                java_home = os.environ["JAVA_HOME"]
                print("JAVA_HOME set to:", java_home)
            except EnvironmentError as e:
                print(f"Error: {e}")

        if not java_home:
            print("JAVA_HOME is still not set. Please set it manually.")
            return

        # Check if ANDROID_HOME is set
        android_home = os.environ.get("ANDROID_HOME")

        if not android_home:
            print("ANDROID_HOME environment variable is not set. Setting it now...")
            try:
                android_sdk_path = find_sdk_directory()
                if android_sdk_path is None:
                    print("SDK Path Not Found")
                    return
                os.environ["ANDROID_HOME"] = android_sdk_path
                android_home = os.environ["ANDROID_HOME"]
                print("ANDROID_HOME set to:", android_home)
            except EnvironmentError as e:
                print(f"Error: {e}")

        if not android_home:
            print("ANDROID_HOME is still not set. Please set it manually.")
            return

        # Check Android SDK paths
        android_sdk_paths = [
            os.path.join(android_home, "platform-tools"),
            # os.path.join(android_home, "build-tools"),
            # Add more paths as needed
        ]

        for path in android_sdk_paths:
            if not os.path.exists(path):
                raise EnvironmentError(f"Android SDK path not found: {path}")

    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)


def is_appium_doctor_installed():
    try:
        # Run 'appium-doctor --version' and capture the output
        appium_doctor_version = subprocess.run(
            ["appium-doctor", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            shell=True,
            text=True,
        )

        # Check if the command ran successfully
        if appium_doctor_version.returncode == 0:
            return True
        else:
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If there was an error or 'appium-doctor' was not found, return False
        return False


def install_appium_doctor():
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            subprocess.run(
                ["npm", "install", "-g", "appium-doctor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            subprocess.run(
                ["npm", "install", "-g", "allure-commandline"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )

        else:  # Linux and macOS
            subprocess.run(
                ["npm", "install", "-g", "appium-doctor"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            subprocess.run(
                ["npm", "install", "-g", "allure-commandline"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        print("Appium Doctor & allure command line Installed...")
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def check_and_install_dependency():
    print(f"Your Platform is {sys.platform}")
    try:
        if (
                sys.platform == "darwin"
                or sys.platform == "linux"
                or sys.platform == "linux2"
        ):  # macOS
            update_command = "apt update"
            execute_sudo_command(update_command)
            if not is_curl_installed():
                print("Curl are not installed. Installing curl...")
                install_curl()

                # Recheck if Node.js and npm are installed after the installation
                if not is_curl_installed():
                    print("Curl installation failed. Please install Curl manually.")
                    return
                else:
                    print("Curl installation successful.")
            else:
                print("Curl Found, Skipping Installation...")
        elif sys.platform == "win32":  # Windows
            choco_version = check_chocolatey_installed()
            if choco_version is None:
                install_chocolatey()
                print(f"Chocolatey is installed. Version: {choco_version}")
            else:
                print("Chocolatey is already there...")
            if check_chocolatey_installed() is None:
                print("Something is wrong, Install Choco Manually...")
                return

        else:
            return False  # Unsupported platform
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    if not is_homebrew_installed():
        return
    if not is_nodejs_installed():
        print("Node.js and/or npm are not installed. Installing Node.js...")
        install_nodejs()

    current_node_version = get_node_version()
    if current_node_version is None:
        return
    elif current_node_version < "18.0.0":
        print(
            "Node.js and/or npm is not up to date. Update Node.js Manually Then Continue..."
        )
        return
    else:
        print(f"Node {current_node_version} is already installed.")

    current_appium_version = get_appium_version()
    if current_appium_version is None:
        install_appium()
    elif current_appium_version < "2.0.0":
        update_appium()
    else:
        print(f"Appium {current_appium_version} is already installed.")
    jdk_installed, jre_installed = check_java()
    if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":
        if jdk_installed and jre_installed:
            path = find_java_jdk_path()
            print(f"JDK Path: {path}")
        else:
            print("JDK or JRE is not installed. Now Installing...")
            install_java()
            if not check_java():
                return
            print("JDK or JRE is installed....")

    else:
        path = find_java_jdk_path()
        print(f"JDK Path: {path}")
        print("Couldn't Check Java Version...")
    sdk_installed = check_sdk()

    if not sdk_installed:
        print(
            "Android SDK is not installed or not found in common locations. Now Installing..."
        )
        install_sdk()
        print("Android SDK Installed...")
        check_sdk()
    check_environment()

    if not is_appium_doctor_installed():
        install_appium_doctor()
    subprocess.run(
        ["appium-doctor"],
        check=True,
        shell=True,
    )


if __name__ == "__main__":
    check_and_install_dependency()
