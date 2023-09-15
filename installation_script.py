import json
import re
import shutil
import subprocess
import platform


class InstallationError(Exception):
    def __init__(self, package, message):
        self.package = package
        self.message = message
        super().__init__(self.message)


class PackageManagerNotFound(Exception):
    def __init__(self, package_manager):
        self.package_manager = package_manager
        self.message = f"{package_manager} package manager not found. Please install it and try again."
        super().__init__(self.message)


def get_package_manager():
    system_platform = platform.system().lower()
    if system_platform == "windows":
        package_manager = "choco"
    elif system_platform == "linux":
        package_manager = "apt" if shutil.which("apt-get") else "brew" if shutil.which("brew") else None
    elif system_platform == "darwin":
        package_manager = "brew"
    else:
        raise InstallationError("Unsupported operating system")

    # Check if the selected package manager is available in the system
    if package_manager is None:
        raise PackageManagerNotFound("apt or brew")

    try:
        subprocess.run(
            [package_manager, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            shell=system_platform == "windows",  # Use shell=True only for Windows
        )
        return package_manager
    except subprocess.CalledProcessError:
        raise PackageManagerNotFound(package_manager)


def handle_sub_package(sub_package_name, install_command, update_command, uninstall_command):
    # Install the sub-package
    try:
        print(f"Installing {sub_package_name}...")
        subprocess.run(
            install_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            shell=True,
        )
        print(f"{sub_package_name} has been successfully installed.")
    except subprocess.CalledProcessError:
        print(f"An error occurred while installing {sub_package_name}.")

    # Update the sub-package (if an update command is provided)
    if update_command:
        try:
            print(f"Updating {sub_package_name}...")
            subprocess.run(
                update_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            print(f"{sub_package_name} has been updated to the latest version.")
        except subprocess.CalledProcessError:
            print(f"An error occurred while updating {sub_package_name}.")

    # Uninstall the sub-package (if an uninstall command is provided)
    if uninstall_command:
        try:
            print(f"Uninstalling {sub_package_name}...")
            subprocess.run(
                uninstall_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            print(f"{sub_package_name} has been uninstalled.")
        except subprocess.CalledProcessError:
            print(f"An error occurred while uninstalling {sub_package_name}.")


def check_and_install_or_update(package_details):
    package_name = package_details["name"]
    check_commands = package_details["check_commands"]
    install_commands = package_details["install_commands"]
    update_commands = package_details["update_commands"]
    uninstall_commands = package_details.get("uninstall_commands", {})
    min_version = package_details.get("min_version", None)
    sub_packages = package_details.get("sub_packages", [])

    # Define the order of package managers to try
    package_managers_order = ["brew", "choco", "apt", "npm"]
    # Get the selected package manager
    package_manager = get_package_manager()
    installed = False  # Initialize a flag to check if the package is installed

    for check_command in check_commands:
        try:
            # Check if the package is already installed
            version_output = subprocess.check_output(
                check_command,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
            )
            pattern = r'(\d+\.\d+(\.\d+)?)'
            match = re.search(pattern, version_output.strip())
            installed_version = match.group(1)

            if min_version:
                # Check if the installed package version is lower than the required minimum version
                installed_version_u = list(map(int, installed_version.split('.')))
                min_version_u = list(map(int, min_version.split('.')))

                if installed_version_u < min_version_u:
                    update_choice = input(
                        f"{package_name} is below the required minimum version {min_version}. Do you want to update it? (yes/no): ").strip().lower()
                    converted_package = re.sub(r'[^a-zA-Z0-9]', '', package_name.lower())
                    if update_choice in {"yes", "y"} and any(
                            converted_package in cmd for cmd in update_commands.values()):
                        print(f"{package_name} updating with {package_manager}...")
                        try:
                            subprocess.run(
                                update_commands[converted_package],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                shell=True,
                            )
                            print(f"{package_name} has been updated to the latest version.")
                        except subprocess.CalledProcessError:
                            print(f"An error occurred while updating {package_name}.")
                    else:
                        print(f"Operation canceled. Please update {package_name} and try again.")
                        return False  # Return failure status

                installed = True  # Package is installed and meets the minimum version
                break  # Exit the loop if a suitable version is found

            installed = True  # Package is installed
            break  # Exit the loop if the package is found

        except subprocess.CalledProcessError:
            continue  # Move to the next check command if this one fails

    if not installed:
        print(f"{package_name} is not installed. Attempting installation...")

        # Iterate through the package managers in order
        for package_manager in package_managers_order:
            if package_manager in install_commands:
                try:
                    print(f"{package_name} installing with {package_manager}...")
                    subprocess.run(
                        install_commands[package_manager],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True,
                        shell=True,
                    )
                    print(f"{package_name} has been successfully installed.")

                    if package_name == "Appium" and package_manager == "npm":
                        # Execute 'appium driver list' and show its output
                        appium_driver_list_output = subprocess.check_output(
                            "appium driver list",
                            stderr=subprocess.STDOUT,
                            shell=True,
                            text=True,
                        )
                        print("Available Appium drivers:")
                        print(appium_driver_list_output)
                        # Ask the user if they want to install 'appium driver'
                        install_appium_driver = input(
                            "Do you want to install 'appium driver'? (yes/no): ").strip().lower()
                        if install_appium_driver in {"yes", "y"}:
                            print("Installing 'appium driver'...")
                            subprocess.run(
                                install_commands.get("appium driver", ""),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                shell=True,
                            )
                            print("'appium driver' has been successfully installed.")

                            # Ask the user to choose sub-packages to install
                            print(f"Available sub-packages for {package_name}:")
                            for i, sub_package in enumerate(sub_packages, start=1):
                                print(f"{i}. {sub_package['name']}")

                            while True:
                                try:
                                    user_choice = input(
                                        f"Choose a sub-package to install (1-{len(sub_packages)}) or 'exit' to finish: ").strip()
                                    if user_choice.lower() == 'exit':
                                        break  # Exit the loop if the user chooses to finish

                                    user_choice = int(user_choice)
                                    if 1 <= user_choice <= len(sub_packages):
                                        selected_sub_package = sub_packages[user_choice - 1]
                                        sub_package_name = selected_sub_package["name"]
                                        sub_package_install_command = selected_sub_package.get("install_command")

                                        # Install the selected sub-package
                                        if sub_package_install_command:
                                            print(f"Installing {sub_package_name}...")
                                            subprocess.run(
                                                sub_package_install_command,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                check=True,
                                                shell=True,
                                            )
                                            print(f"{sub_package_name} has been successfully installed.")
                                        else:
                                            print(f"No install command found for {sub_package_name}.")

                                    else:
                                        print("Invalid choice. Please enter a valid number or 'exit' to finish.")
                                except (ValueError, IndexError):
                                    print("Invalid input. Please enter a number or 'exit' to finish.")

                    return True  # Return success status

                except subprocess.CalledProcessError:
                    print(f"An error occurred while installing {package_name} with {package_manager}.")

    else:
        print(f"{package_name} is already installed.")
        return True  # Return success status


def load_packages_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            packages = json.load(file)
        return packages
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def check_and_install_env(package_file_path):
    packages_to_install_or_update = load_packages_from_file(package_file_path)

    if not packages_to_install_or_update:
        print("No packages found in the file.")
        return

    for package_details in packages_to_install_or_update:
        success = check_and_install_or_update(package_details)
        if not success:
            print(f"Failed to install/update {package_details['name']}. Aborting further execution.")
            return


# Call the function to check and install or update the environment
if __name__ == "__main__":
    check_and_install_env('packages.json')
