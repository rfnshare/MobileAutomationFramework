import subprocess
from pathlib import Path

import pytest

from utils.common import read_date, read_time, clean_directory


def run_pytest_tests(test_files):
    report_file_name_prefix = f"{read_date()}_{read_time()}"
    report = (
            Path(__file__).parent.parent
            / f"reports/htmlreport/regression_{report_file_name_prefix}_report.html"
    )
    exit_code = pytest.main(
        test_files + ["-s", f"--html={report}", "--capture=tee-sys"]
    )
    if exit_code == 0:
        print("All tests passed successfully.")
    else:
        print("Some tests failed.")
    # html report open
    html_open_report = f"start {report}"
    subprocess.run(html_open_report, shell=True)


if __name__ == "__main__":
    clean_directory(Path(__file__).parent.parent / "reports")
    test_files_to_run = ["test_android/test_sample.py::TestHomePage::test_fill_form"]
    run_pytest_tests(test_files_to_run)

# run by marker -m
# run by keyword search -k
# pytest -s -n 4 --alluredir=report.html --self-contained-html testcase
