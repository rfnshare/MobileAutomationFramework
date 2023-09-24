Before running installation_script.py these need to set up manually
# For Linux
- Install Curl
  - sudo apt install curl   
- Install Git, pip3 [Install pip3, if pip3 is not there]
  - sudo apt install git, sudo apt install python3-pip
- Install Homebrew (Package Manager) For Linux & macOS
  - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#  For macOS
- TBA

# For Windows
- Install chocolatey
  - Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
- Install Git
  - choco install git -y
- Install Python
  - choco install python -y
- Install Windows Terminal [Recommended From Store]

# Known Issues

1. [x] Linux
  - Appium 2.0 already installed but driver are not installed (can't handle this logic)
  - tqdm import error although tqdm installed.
2. [x] Windows
  - Powershell throw error after node install, can't detect node after immediate install
3. [x] Mac
  - Add JAVA & Android Path into functions
4. [x] Common
  - TBA

# Pending Work
- Testing On Mac (Pending: Add JAVA & SDK path into functions)
- Need to handle update in different way. Remove existing in any way then install again.
- Need to handle uninstall efficiently

