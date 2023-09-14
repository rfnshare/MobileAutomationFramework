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
    check_command = package_details["check_command"]
    install_commands = package_details["install_commands"]
    update_commands = package_details.get("update_commands", {})
    min_version = package_details.get("min_version", None)

    try:
        # Check if the package is already installed
        subprocess.run(
            check_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            shell=True,
        )
        print(f"{package_name} is already installed.")
        return True  # Return success status

    except subprocess.CalledProcessError:
        print(f"{package_name} is not installed. Attempting installation...")

        # Get the selected package manager
        package_manager = get_package_manager()

        # Select the appropriate installation or update command based on the package manager
        if package_manager not in install_commands:
            print(f"Unsupported package manager '{package_manager}' for {package_name}. Skipping installation.")
            return False  # Return failure status

        try:
            subprocess.run(
                install_commands[package_manager],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                shell=True,
            )
            print(f"{package_name} has been successfully installed.")
        except subprocess.CalledProcessError:
            print(f"An error occurred while installing {package_name} with {package_manager}.")
            return False  # Return failure status

        if min_version:
            # Check if the installed package version is lower than the required minimum version
            try:
                version_output = subprocess.check_output(
                    check_command,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    text=True,
                )
                installed_version = version_output.strip().split()[-1]  # Extract the version number
                installed_version = tuple(map(int, installed_version.split(".")))  # Convert to tuple

                if installed_version < min_version:
                    update_choice = input(
                        f"{package_name} is below the required minimum version {min_version}. Do you want to update it? (yes/no): ").strip().lower()
                    if update_choice in {"yes", "y"} and package_manager in update_commands:
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

            except subprocess.CalledProcessError:
                print(f"Failed to check the version of {package_name}.")

        return True  # Return success status


def check_and_install_env():
    # Define the package details inside the function
    packages_to_install_or_update = [
        {
            "name": "Git",
            "check_command": 'git --version',
            "install_commands": {
                "choco": "choco install git -y",
                "apt": "sudo apt-get install git",
                "brew": "brew install git",
            },
            "update_commands": {
                "choco": "choco upgrade git -y",
                "apt": "sudo apt upgrade git",
                "brew": "brew upgrade git",
            },
            "min_version": (2, 0, 0),
        },
        {
            "name": "Python",
            "check_command": 'python --version',
            "install_commands": {
                "choco": "choco install python -y",
                "apt": "sudo apt-get install python",
                "brew": "brew install python",
            },
            "update_commands": {
                "choco": "choco upgrade python -y",
                "apt": "sudo apt-get install --only-upgrade python -y",
                "brew": "brew upgrade python",
            },
            "min_version": (3, 8, 0),
        },
        # Add more packages as needed
    ]

    try:
        # Check if the required package manager is available
        get_package_manager()
    except PackageManagerNotFound as e:
        print(e.message)
        print("Please install the required package manager and try again.")
        return

    for package_details in packages_to_install_or_update:
        try:
            check_and_install_or_update(package_details)
        except InstallationError as e:
            print(e.message)
            print(f"{e.package} installation failed. Aborting further execution.")
            return

    # Continue with your desired workflow here.
    # This code will only execute if all packages are successfully installed or updated.


# Call the function to check and install or update the environment
if __name__ == "__main__":
    check_and_install_env()
