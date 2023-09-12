# import os
# import subprocess
# import re
# import json
#
#
# def is_nodejs_installed():
#     try:
#         system_platform = os.name
#         if system_platform == "nt":  # Windows
#             subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
#                            shell=True)
#             subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
#         else:  # Linux and macOS
#             subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#             subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#         return True
#     except subprocess.CalledProcessError:
#         return False
#     except Exception as e:
#         print(f"An error occurred while checking Node.js and npm: {e}")
#         return False
#
#
# def install_nodejs():
#     system_platform = os.name
#
#     if system_platform == "posix":  # Linux and macOS
#         # Check if Node.js is already installed
#         try:
#             subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#             subprocess.run(["npm", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#             print("Node.js and npm are already installed. Skipping installation.")
#         except subprocess.CalledProcessError:
#             # Install Node.js and npm using the appropriate package manager for Linux/macOS
#             package_managers = ["apt", "brew", "yum"]
#             installed_manager = None
#
#             for manager in package_managers:
#                 try:
#                     password = 'your_password_here\n'  # Replace with the actual password
#                     update_command = ["sudo", "-S", manager, "update"]
#                     curl_install_command = ["sudo", "-S", manager, "install", "curl"]
#                     install_command = ["sudo", "-S", manager, "install", "-y", "nodejs"]
#
#                     # Run the update command with sudo
#                     subprocess.run(update_command, input=password, text=True)
#
#                     # Run the curl command to download the setup script
#                     curl_command = ["curl", "-fsSL", "https://deb.nodesource.com/setup_lts.x"]
#                     curl_process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#                     # Run the sudo command to execute the setup script
#                     sudo_command = ["sudo", "-E", "bash", "-"]
#                     subprocess.Popen(sudo_command, stdin=curl_process.stdout, stdout=subprocess.PIPE,
#                                                     stderr=subprocess.PIPE)
#                     subprocess.run(curl_install_command, input=password, text=True)
#                     # Run the install command with sudo
#                     subprocess.run(install_command, input=password, text=True)
#
#                     installed_manager = manager
#                     break
#                 except FileNotFoundError:
#                     continue
#
#             if installed_manager:
#                 print(f"Node.js and npm installed using {installed_manager}.")
#             else:
#                 print("Node.js installation failed. Please install Node.js and npm manually.")
#     elif system_platform == "nt":  # Windows
#         # Check if Node.js is already installed
#         if not is_nodejs_installed():
#             print("Node.js and npm are not installed. Installing Node.js...")
#
#             # Download and run the official Node.js installer for Windows
#             nodejs_installer_url = "https://nodejs.org/dist/latest/node-v16.13.0-x64.msi"  # Update URL with the latest LTS version
#             nodejs_installer_path = os.path.expanduser("~/node_installer.msi")
#
#             # Download the Node.js installer
#             subprocess.run(["curl", "-o", nodejs_installer_path, nodejs_installer_url])
#
#             # Run the installer silently
#             subprocess.run(["msiexec", "/i", nodejs_installer_path, "/qn", "/L*V", "node_install.log"])
#
#             # Clean up the installer file
#             os.remove(nodejs_installer_path)
#
#             # Verify Node.js and npm installation
#             if not is_nodejs_installed():
#                 print("Node.js installation failed. Please install Node.js and npm manually.")
#                 return
#             else:
#                 print("Node.js and npm installation successful.")
#         else:
#             print("Node.js is already installed. Skipping installation.")
#     else:
#         print("Unsupported operating system")
#         return
#
#
# def get_appium_version():
#     try:
#         system_platform = os.name
#         if system_platform == "nt":  # Windows
#             result = subprocess.run(["appium", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
#                                     check=True, shell=True)
#         else:  # Linux and macOS
#             result = subprocess.run(["appium", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
#                                     check=True)
#
#         version_match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
#         if version_match:
#             return version_match.group(1)
#         else:
#             return None
#     except (FileNotFoundError, subprocess.CalledProcessError):
#         return None
#
#
# def install_appium_version(system_platform):
#     if system_platform == "posix":  # Linux and macOS
#         # Install Appium globally for Linux and macOS
#         subprocess.run(["npm", "install", "-g", "appium"])
#     elif system_platform == "nt":  # Windows
#         # Install Appium globally for Windows
#         subprocess.run(["npm", "install", "-g", "appium"])
#     else:
#         print("Unsupported operating system")
#
#
# def install_appium_drivers(system_platform):
#     # Add your logic for installing Appium drivers here
#     if system_platform == "posix":  # Linux and macOS
#         # Install the required Appium drivers for Linux and macOS
#         subprocess.run(["appium", "driver", "install", "uiautomator2"])
#         subprocess.run(["appium", "driver", "install", "xcuitest"])
#     elif system_platform == "nt":  # Windows
#         # Install the required Appium drivers for Windows
#         subprocess.run(["appium", "driver", "install", "uiautomator2"], shell=True)
#         subprocess.run(["appium", "driver", "install", "xcuitest"], shell=True)
#     else:
#         print("Unsupported operating system")
#
#
# def install_appium():
#     system_platform = os.name
#
#     if not is_nodejs_installed():
#         print("Node.js and/or npm are not installed. Skipping Appium installation.")
#         return
#
#     current_version = get_appium_version()
#
#     if current_version:
#         print(f"Appium {current_version} is already installed.")
#
#         if current_version < "2.0.0":
#             user_response = input(
#                 "Appium version is older than 2.0.0. Do you want to uninstall the existing Appium and install the latest version? (yes/no): ").strip().lower()
#
#             if user_response == "yes":
#                 if system_platform == "posix":  # Linux and macOS
#                     subprocess.run(["npm", "uninstall", "-g", "appium"])
#                 elif system_platform == "nt":  # Windows
#                     subprocess.run(["npm", "uninstall", "-g", "appium", "--global-style"])
#                 print("Uninstalling the existing Appium...")
#
#                 # Reinstall Appium
#                 install_appium_version(system_platform)
#             else:
#                 print("Skipping Appium installation.")
#                 return
#         else:
#             print(f"Appium version {current_version} is up to date.")
#     else:
#         # Appium is not installed, install it
#         install_appium_version(system_platform)
#
#     # Check the installed Appium version again
#     updated_version = get_appium_version()
#
#     if updated_version and updated_version >= "2.0.0":
#         print("Appium installation/Checked complete.")
#         install_appium_drivers(system_platform)
#         print("Appium driver installation/checked complete.")
#
#
# def check_and_install_dependency():
#     system_platform = os.name
#
#     if not is_nodejs_installed():
#         print("Node.js and/or npm are not installed. Installing Node.js...")
#         install_nodejs()
#
#         # Recheck if Node.js and npm are installed after the installation
#         if not is_nodejs_installed():
#             print("Node.js installation failed. Please install Node.js and npm manually.")
#             return
#         else:
#             print("Node.js and npm installation successful.")
#
#     install_appium()
#
#
# if __name__ == "__main__":
#     install_appium()
