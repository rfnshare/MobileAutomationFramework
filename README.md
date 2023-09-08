[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->

<br />
<p align="center">
  <a href="https://github.com/rfnshare/workspace-laznormal">
    <img src="logo.png" alt="Logo" height="100">
  </a>

  <h3 align="center">App Automation</h3>

  <p align="center">
    ...
    <br />
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/rfnshare/upay/issues">Report Bug</a>
    ·
    <a href="#">Request Feature</a>
  </p>
Introduction

This is an appium based framework that interacts with upay Android App and can be used to automate given below

1. Login Into App
2. **Send Money**
3. Mobile Recharge
4. Make Payment
5. Cash Out

# Project Structure
The project structure follows POM and is organized as follows:

- **Pages Directory:** Contains page objects corresponding to the application's UI pages.
- **Utils Directory:** Houses locators, test data, and common functions for the test automation framework.
- **Tests Directory:** Includes test cases for various functionalities.

# Features
- **Logging Feature:** The framework includes a logging feature for better visibility into test execution.
- **HTML Report:** Test results are presented in an HTML report, making it easy to review the outcomes.
- **Screenshot Capture:** In case of test failures, screenshots are automatically added to the HTML report. Passed screenshots are also saved in the reports directory for future reference.
- **Data-driven testing** is implemented using Excel for login scenarios.
- **APK File:** The APK file of the application under test is stored in the app directory.
- **Jenkins Integration:** Jenkins integration is included, allowing you to execute test cases from the Jenkins dashboard.

# Setup

Dependency Software List:
- Appium Server 2.0.0
- Java version "20.0.0"
- Android Studio (Optional)
- Node.js (18) and npm (9.6.7)
- Android SDK
- ADB (Android Debug Bridge)
- WebDriver Library (Appium-Python-Client)

1. Extract this repository
    ```
   Ignore
    git clone https://github.com/rfnshare/upay.git
    ```

2. If you clone this repository before then run this on the project's root directory
    ```
    git pull
    ```
3. Copy APK file, create a folder name apk in project root directory & paste it in project apk folder.
    ```
    apk/appname.apk
    ```
   Make sure you connect you android device/emulator & set uid in tests/conftest.py.
4. Go to the project's root directory and install requirements(Recommended create virtual env first).
    ```
    pip install -r requirements.txt
    ```
   
5. For Run All, Run tests/test_android/final script.
    ```
    Inside tests/test_android/final.py, test_files_to_run
    Add your classname, function or python file name

    ```
   This will open an app in the android device & run regression test.

7. Generate allure reports with run script include log.
    ```
    HTML Report added, it will generate automatically with log. 
    Allure report will added later.
    ```
   This will create an HTML/allure report. You can find report in project's root directory

### Usage


For more examples,  please refer to the [Documentation](https://example.com)

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/rfnshare/upay/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request

<!-- CONTACT -->
## Contact

Abdullah Al Faroque - [@rfnshare](https://twitter.com/rfnshare) - aalfaroque@gmail.com

Project Link: [Android Automation](https://github.com/rfnshare/upay.git)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-0-yellow?style=for-the-badge
[contributors-url]: https://github.com/rfnshare/workspace-laznormal/graphs/contributors
[forks-shield]: https://img.shields.io/badge/froks-0-blue?style=for-the-badge
[forks-url]: https://github.com/rfnshare/workspace-laznormal/network/members
[stars-shield]: https://img.shields.io/badge/stars-0-red?style=for-the-badge
[stars-url]: https://github.com/rfnshare/workspace-laznormal/stargazers
[issues-shield]: https://img.shields.io/badge/issues-0-success?style=for-the-badge
[issues-url]: https://github.com/rfnshare/workspace-laznormal/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/rfnshare