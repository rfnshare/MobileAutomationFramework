import os
import platform
import subprocess
import sys
import getpass


def execute_sudo_command(command):
    sudo_password = getpass.getpass("Enter your sudo password: ")
    p = os.system('echo %s|sudo -S %s' % (sudo_password, command))
    if p == 0:
        return True
    else:
        return False


def is_curl_installed():
    try:
        subprocess.run(["curl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_curl():
    system_platform = platform.system()

    if system_platform == "Windows":
        print("Curl installation on Windows is not supported via Python script.")
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
            subprocess.run(["brew", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
            # Check if Homebrew is installed on Linux
            homebrew_install_path = "/home/linuxbrew/.linuxbrew/bin/brew"
            subprocess.run([homebrew_install_path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           check=True)
            return True
        elif sys.platform == "win32":  # Windows
            # Check if Homebrew is installed on Windows
            homebrew_install_path = r"C:\Program Files\Git\usr\bin\brew.exe"  # Update with the actual path
            subprocess.run([homebrew_install_path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           check=True)
            return True
        else:
            return False  # Unsupported platform
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_homebrew():
    pass  # will implement later, now install manually


def check_and_install_dependency():
    # execute_sudo_command("apt update")
    # if is_homebrew_installed():
    #     print("Homebrew is installed. You can continue with your Homebrew-related tasks.")
    #     # Add your Homebrew-related tasks here
    # else:
    #     print("Homebrew is not installed. Please install Homebrew and then continue.")
    #     # Add instructions or code for installing Homebrew here
    try:
        if sys.platform == "darwin" or sys.platform == "linux" or sys.platform == "linux2":  # macOS
            if not is_curl_installed():
                print("Curl are not installed. Installing curl...")
                install_curl()

                # Recheck if Node.js and npm are installed after the installation
                if not is_curl_installed():
                    print("Curl installation failed. Please install Curl manually.")
                    return
                else:
                    print("Curl and npm installation successful.")
            else:
                print("Curl Found, Skipping Installation...")
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
        return False


# Example usage:
if __name__ == "__main__":
    check_and_install_dependency()
