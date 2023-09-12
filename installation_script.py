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
        print("Curl installation on Windows is not supported via Python script. Do it manually")
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
            print("Homebrew is found. You can continue with your Homebrew-related tasks.")
            return True
        elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
            # Check if Homebrew is installed on Linux
            homebrew_install_path = "/home/linuxbrew/.linuxbrew/bin/brew"
            subprocess.run([homebrew_install_path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           check=True)
            print("Homebrew is found. You can continue with your Homebrew-related tasks.")
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


def install_homebrew():
    pass  # will implement later, now install manually


def is_nodejs_installed():
    try:
        system_platform = os.name
        if system_platform == "nt":  # Windows
            node_version = subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          check=True,
                                          shell=True)
            npm_version = subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         check=True, shell=True)
            print(f"Found Nodejs {node_version.stdout.strip()} & npm {npm_version.stdout.strip()}")
        else:  # Linux and macOS
            node_version = subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          check=True)
            npm_version = subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         check=True)
            print(f"Found Nodejs {node_version.stdout.strip()} & npm {npm_version.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"An error occurred while checking Node.js and npm")
        return False


def install_nodejs():
    system_platform = os.name

    if system_platform == "posix":  # Linux and macOS
        try:
            update_command = "apt update"
            install_command = ["brew", "install", "nodejs"]
            execute_sudo_command(update_command)
            subprocess.run(install_command)

        except FileNotFoundError:
            print("Node.js installation failed. Please install Node.js and npm manually.")
            return None
    elif system_platform == "nt":  # Windows
        # Download and run the official Node.js installer for Windows
        nodejs_installer_url = "https://nodejs.org/dist/latest/node-x64.msi"
        nodejs_installer_path = os.path.expanduser("~/node-setup.msi")
        # Download the Node.js installer
        subprocess.run(["curl", "-o", nodejs_installer_path, nodejs_installer_url])
        # Run the installer silently
        subprocess.run(["msiexec", "/i", nodejs_installer_path, "/qn", "/L*V", "node_install.log"])
        # Clean up the installer file
        os.remove(nodejs_installer_path)
    else:
        print("Unsupported operating system")
        return

    # Verify Node.js and npm installation
    if not is_nodejs_installed():
        print("Node.js installation failed. Please install Node.js and npm manually.")
        return
    else:
        print("Node.js and npm installation successful.")


def check_and_install_dependency():
    print(f"Your Platform is {sys.platform}")
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
                    print("Curl installation successful.")
            else:
                print("Curl Found, Skipping Installation...")
        elif sys.platform == "win32":  # Windows
            print("Curl Check Skipping For Now For Windows")
        else:
            return False  # Unsupported platform
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    is_homebrew_installed()

    if not is_nodejs_installed():
        print("Node.js and/or npm are not installed. Installing Node.js...")
        install_nodejs()


# Example usage:
if __name__ == "__main__":
    check_and_install_dependency()
