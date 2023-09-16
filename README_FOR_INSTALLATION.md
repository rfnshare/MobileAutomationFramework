Before running installation_script.py these need to set up manually
# For Linux & macOS
- Install Curl
  - sudo apt install curl   
- Install Homebrew (Package Manager) For Linux & macOS
  - /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# For Windows
- Install chocolatey
  - Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
- Install Python
  - choco install python

# Known Issues

1. [x] Linux
  - Appium already installed but driver are not installed (can't handle this logic)
2. [x] Windows
  - TBA
3. [x] Common 
  - Java & Android Update Handle

# Pending Work
- Testing On Mac

