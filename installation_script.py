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
        sub_package_manager = "npm"
    elif system_platform == "linux":
        sub_package_manager = "npm"
        package_manager = "apt" if shutil.which("apt-get") else "brew" if shutil.which("brew") else "npm"
    elif system_platform == "darwin":
        package_manager = "brew"
        sub_package_manager = "npm"
    else:
        raise InstallationError("Unsupported operating system")

    # Check if the selected package manager is available in the system
    if package_manager is None:
        raise PackageManagerNotFound("apt, brew, or npm")

    try:
        subprocess.run(
            [package_manager, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            shell=system_platform == "windows",  # Use shell=True only for Windows
        )
        return package_manager, sub_package_manager
    except subprocess.CalledProcessError:
        raise PackageManagerNotFound(package_manager)


def execute_command(command):
    try:
        return subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None


def is_installed(package_name, check_commands, min_version=None):
    for check_command in check_commands:
        version_output = execute_command(check_command)
        if version_output:
            pattern = r'(\d+\.\d+(\.\d+)?)'
            match = re.search(pattern, version_output.strip())
            installed_version = match.group(1)

            if min_version:
                installed_version_u = list(map(int, installed_version.split('.')))
                min_version_u = list(map(int, min_version.split('.')))

                if installed_version_u < min_version_u:
                    return False, installed_version  # Return the installed version
            return True, installed_version  # Return the installed version

    return False, None  # Return False if no version information is found


def update_package(package_name, package_manager, sub_package_manager, update_commands):
    converted_package = re.sub(r'[^a-zA-Z0-9]', '', package_name.lower())
    print(f"{package_name} updating with {package_manager}...")
    # Try to update using the primary package manager
    if package_manager in update_commands:
        try:
            subprocess.run(
                update_commands[package_manager],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            return True
        except subprocess.CalledProcessError:
            pass  # Continue to the next update attempt

    # Try to update using the fallback sub_package_manager
    if sub_package_manager in update_commands:
        try:
            subprocess.run(
                update_commands[sub_package_manager],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            return True
        except subprocess.CalledProcessError:
            pass  # Both update attempts failed

    return False


def install_package(package_name, package_manager, install_commands):
    if package_manager in install_commands:
        try:
            subprocess.run(
                install_commands[package_manager],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False
    return False


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

    # Uninstall the sub-package (if an uninstallation command is provided)
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

    package_managers_order = ["brew", "choco", "apt", "npm"]
    package_manager, sub_package_manager = get_package_manager()
    installed = False

    # Check if the package is already installed
    is_installed_result, installed_version = is_installed(package_name, check_commands, min_version)
    if is_installed_result:
        if package_name == "Appium":
            print(f"{package_name} is already installed.")
            appium_driver_list_output = execute_command("appium driver list")
            if appium_driver_list_output:
                print(appium_driver_list_output)
        else:
            print(f"{package_name} is already installed.")
        return True
    # try to update the package if the user chooses to
    if installed_version is not None and not is_installed_result:
        update_choice = input(
            f"{package_name} is below the required minimum version {min_version}. Do you want to update it? (yes/no): ").strip().lower()
        if update_choice in {"yes", "y"}:
            if update_package(package_name, package_manager, sub_package_manager, update_commands):
                print(f"{package_name} has been updated to the latest version.")
                return True
        else:
            print(f"Operation canceled. Please update {package_name} and try again.")
            return False  # Return failure status
    print(f"{package_name} is not installed. Attempting installation...")

    for package_manager in package_managers_order:
        if install_package(package_name, package_manager, install_commands):
            if package_name == "Appium" and package_manager == "npm":
                appium_driver_list_output = execute_command("appium driver list")
                if appium_driver_list_output:
                    # print("Available Appium drivers:")
                    # Check if the text is present before removing it
                    # result = appium_driver_list_output.replace("âœ”", "").strip()
                    print(appium_driver_list_output)

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
                                        break

                                    user_choice = int(user_choice)
                                    if 1 <= user_choice <= len(sub_packages):
                                        selected_sub_package = sub_packages[user_choice - 1]
                                        sub_package_name = selected_sub_package["name"]
                                        sub_package_install_command = selected_sub_package.get("install_command")

                                        if sub_package_install_command:
                                            print(f"Installing {sub_package_name}...")
                                            if install_package(sub_package_name, package_manager,
                                                               sub_package_install_command):
                                                print(f"{sub_package_name} has been successfully installed.")
                                            else:
                                                print(f"Failed to install {sub_package_name}.")
                                        else:
                                            print(f"No install command found for {sub_package_name}.")
                                    else:
                                        print("Invalid choice. Please enter a valid number or 'exit' to finish.")
                                except (ValueError, IndexError):
                                    print("Invalid input. Please enter a number or 'exit' to finish.")
                        else:
                            print("Failed to install 'appium driver'.")
                    return True

    print(f"Failed to install or update {package_name}.")
    return False


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
