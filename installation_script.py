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


def check_and_install_or_update(package_details):
    package_name = package_details["name"]
    check_commands = package_details["check_commands"]
    install_commands = package_details["install_commands"]
    update_commands = package_details["update_commands"]
    min_version = package_details.get("min_version", None)

    # Define the order of package managers to try
    package_managers_order = ["brew", "choco", "apt"]

    installed = False  # Initialize a flag to check if the package is installed
    # Get the selected package manager
    package_manager = get_package_manager()
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
                    if update_choice in {"yes", "y"} and any(converted_package in cmd for cmd in update_commands.values()):
                        print(f"{package_name} updating with {package_manager}...")
                        try:
                            subprocess.run(
                                update_commands[package_manager],
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
                    return True  # Return success status

                except subprocess.CalledProcessError:
                    print(f"An error occurred while installing {package_name} with {package_manager}.")

        print(f"Failed to install {package_name} with all available package managers.")
        return False  # Return failure status

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
