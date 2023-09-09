[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->

<br />
<p align="center">
  <a href="https://github.com/rfnshare/MobileAutomationFramework">
    <img src="logo.png" alt="Logo" height="225">
  </a>

  <h3 align="center">Test Automation Framework Template (Mobile)</h3>

  <p align="center">
    ...
    <br />
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/rfnshare/MobileAutomationFramework/issues">Report Bug</a>
    ·
    <a href="#">Request Feature</a>
  </p>


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
**Download JDK**

Download From https://www.oracle.com/java/technologies/downloads/

Install the JDK on your machine

Also, set Environment Variables 

**Download ANDROID SDK**

Download sdk  From https://developer.android.com/studio

Set ANDROID_HOME as environment variable by adding mentioned path in .bashrc file

          - export ANDROID_HOME=/home/user/Android/Sdk
 
Also set path variables by following by adding :

         - export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

**Appium Installation:**

You can follow following link for installation https://medium.com/@syamsasi/setting-up-appium-on-windows-and-ubuntu-ea9a73ab989
 
**Pycharm Installation:**

Download the Pycharm from their official website.

Install the Pycharm on your machine.

1. Clone this repository
    ```
    git clone https://github.com/rfnshare/MobileAutomationFramework
    ```

2. If you clone this repository before then run this on the project's root directory
    ```
    git pull
    ```
3. Copy your APK file, & paste it in project app folder.
    ```
    app/android/appname.apk
    ```
4. Configure ```config/properties.ini``` file with your APK name. Make sure you connect you android device/emulator. Devices UDID, ApK path, appPackage & appActivity will detect automatically.
5. Go to the project's root directory and install requirements (Recommended create virtual env first).
    ```
    pip install -r requirements.txt
    ```
## Run Automated Tests

* To run all test cases in cmd line with html & allure report, run
```
python -m pytest -m <smoke/regression> --html=reports/htmlreport/index.html --self-contained-html -s --alluredir=reports/allure_report/<smoke/regression>_report_allure
```
* Generate Allure HTML Report
```
allure serve reports/allure_report/<smoke/regression>_report_allure
```
* To run all test cases without cmd line, Go to project root directory then tests folder & run `final.py` file.

This will create an HTML, allure report, automatically attach failed screenshot in report. You can find report in reports directory, report automatically will open in browser.
* You can configure Jenkins to parameterized run your test cases & generate html report, allure report, junit report. Also send mail to recipient (pending for implementation).

## Sample Test Report

![Allure report screenshot](https://raw.githubusercontent.com/startrug/phptravels-selenium-py/screenshots/allure_report.png "Allure report screenshot")

Report is generated in a chosen browser.

### Usage

For more examples,  please refer to the [Documentation](https://example.com)

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/rfnshare/MobileAutomationFramework/issues) for a list of proposed features (and known issues).



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

Portfolio: - [Abdullah Al Faroque](https://rfnshare.github.io/)
Project Link: [Android Automation](https://github.com/rfnshare/MobileAutomationFramework.git)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-0-yellow?style=for-the-badge
[contributors-url]: https://github.com/rfnshare/MobileAutomationFramework/graphs/contributors
[forks-shield]: https://img.shields.io/badge/froks-0-blue?style=for-the-badge
[forks-url]: https://github.com/rfnshare/MobileAutomationFramework/network/members
[stars-shield]: https://img.shields.io/badge/stars-0-red?style=for-the-badge
[stars-url]: https://github.com/rfnshare/MobileAutomationFramework/stargazers
[issues-shield]: https://img.shields.io/badge/issues-0-success?style=for-the-badge
[issues-url]: https://github.com/rfnshare/MobileAutomationFramework/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/rfnshare
