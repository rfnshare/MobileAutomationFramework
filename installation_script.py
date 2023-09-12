import os
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


def check_and_install_dependency():
    execute_sudo_command("apt update")
    if is_homebrew_installed():
        print("Homebrew is installed. You can continue with your Homebrew-related tasks.")
        # Add your Homebrew-related tasks here
    else:
        print("Homebrew is not installed. Please install Homebrew and then continue.")
        # Add instructions or code for installing Homebrew here


# Example usage:
if __name__ == "__main__":
    check_and_install_dependency()
