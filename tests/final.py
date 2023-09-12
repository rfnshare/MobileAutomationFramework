import subprocess
import sys
from pathlib import Path

import pytest

from utils.common import read_date, read_time, clean_directory


def run_pytest_tests(test_files):
    report_file_name_prefix = f"{read_date()}_{read_time()}"
    report_html = (
        Path(__file__).parent.parent
        / f"reports/htmlreport/regression_{report_file_name_prefix}_report.html"
    )
    report_xml = (
        Path(__file__).parent.parent
        / f"reports/xml_report/regression_{report_file_name_prefix}_report.xml"
    )
    report_allure = (
        Path(__file__).parent.parent
        / f"reports/allure_report/regression_{report_file_name_prefix}_report"
    )
    # Construct the pytest command as a list of arguments
    pytest_command = [
        "pytest",
        "--durations=0",
        "-vv",
        "-v",
        "-s",
        f"--html={report_html}",
        "--capture=tee-sys",
        "-v",
        f"--junitxml={report_xml}",
        "-s",
        f"--alluredir={report_allure}",
    ]
    # Combine the pytest command and test files into a single list
    pytest_command += test_files
    # Execute the pytest command as a subprocess
    try:
        subprocess.run(pytest_command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code
    # html report open
    html_open_report = f"start {report_html}"
    subprocess.run(html_open_report, shell=True)

    # send report to receivers email [pending for implementation]

    # allure report serve
    allure_serve_command = f"allure serve {report_allure}"
    subprocess.run(allure_serve_command, shell=True)


if __name__ == "__main__":
    clean_directory(Path(__file__).parent.parent / "reports")
    test_files_to_run = [
        'test_android/test_sample.py::TestHomePage::test_error_msg'
    ]
    run_pytest_tests(test_files_to_run)

# run by marker -m
# run by keyword search -k
# pytest -s -n 4 --alluredir=report.html --self-contained-html testcase
