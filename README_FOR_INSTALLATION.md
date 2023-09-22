Before running installation_script.py these need to set up manually
# For Linux & macOS
- Install Curl
  - sudo apt install curl   
- Install Git
  - sudo apt install git
- Install Homebrew (Package Manager) For Linux & macOS
  - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# For Windows
- Install chocolatey
  - Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
- Install Git
  - choco install git -y
- Install Python
  - choco install python -y

# Known Issues

1. [x] Linux
  - Appium already installed but driver are not installed (can't handle this logic)
  - if pip not install in linux, after pip install, tqdm import error although tqdm installed.
2. [x] Windows
  - Unable to generate install log file.
3. [x] Mac
  - Unable to generate install log file.
4. [x] Common 
  - Need to handle update in different way. Remove existing in any way then install again.
  - Java Install Handle, Update Handle
  - Although Java install, it is trying to install again.
  - Can't find JAVA Path with immediate install, throwing error when set env.
  - Android Install, Update Handle

# Pending Work
- Testing On Mac
- Add progress bar/showing progress for installation/Update/Uninstall (Need Common Function)
- Multiple Install Manager not working
- Printing Info when install

