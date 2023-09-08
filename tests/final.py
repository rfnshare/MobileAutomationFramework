import os
import subprocess
from pathlib import Path

import pytest
from datetime import datetime


def clean_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file: {file_path} - {e}")


# Read current date
def read_date():
    return str(datetime.today().strftime("%Y-%m-%d"))


def read_time():
    return str(datetime.today().strftime("%I-%M-%S-%p"))


def run_pytest_tests(test_files):
    report_file_name_prefix = f"{read_date()}_{read_time()}"
    report = Path(__file__).parent.parent / f'reports/htmlreport/regression_{report_file_name_prefix}_report.html'
    exit_code = pytest.main(test_files + ['-s', f'--html={report}', '--capture=tee-sys'])
    if exit_code == 0:
        print("All tests passed successfully.")
    else:
        print("Some tests failed.")
    # html report open
    html_open_report = f"start {report}"
    subprocess.run(html_open_report, shell=True)


if __name__ == "__main__":
    clean_directory(Path(__file__).parent.parent / "reports")
    test_files_to_run = ['-k'] + [
    ]
    run_pytest_tests([])

# run by marker -m
# run by keyword search -k
