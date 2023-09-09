import glob
import inspect
import logging.config
import os
from datetime import datetime
from pathlib import Path

import pandas as pd


def get_logger():
    config_file_path = Path(__file__).parent.parent / "config/logging.conf"
    project_path = Path(__file__).parent.parent
    # Define a custom log filename
    log_filename = project_path.as_posix() + "/" + "reports/logs/logfile.log"

    # Check if the log directory exists; if not, create it
    log_directory = os.path.dirname(log_filename)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        print(f"Log File Created in {log_directory}")

    logging.config.fileConfig(config_file_path, defaults={"log_filename": log_filename})
    # logger_name = inspect.stack()[1][3]
    # Get the caller's frame
    caller_frame = inspect.currentframe().f_back

    # Extract the caller function name
    logger_name = caller_frame.f_code.co_name
    logger = logging.getLogger(logger_name)
    return logger


def get_test_data(sheet_name):
    excel_path = Path(__file__).parent.parent / "utils/testdata.xlsx"
    df = pd.read_excel(excel_path, sheet_name=sheet_name, dtype=str)
    df_filled = df.fillna("")
    return df_filled.to_dict(orient="records")


def get_html_reports():
    reports = []
    try:
        path = Path(__file__).parent.parent / f"reports/htmlreport/regression_*.html"
        report = os.path.abspath(glob.glob(f"{path}")[-1])
        reports.append(report)
    except Exception as e:
        print("Report not ready, Error", e)
    return reports


# Read current date
def read_date():
    return str(datetime.today().strftime("%Y-%m-%d"))


def read_time():
    return str(datetime.today().strftime("%I-%M-%S-%p"))


def clean_directory(directory):
    exclude_dirs = [
        "screenshots",
        "allure_report",
        "htmlreport",
        "logs",
        "xml_report",
        "failed",
        "passed",
    ]
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file: {file_path} - {e}")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir.lower() not in exclude_dirs:
                try:
                    os.rmdir(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete folder: {dir_path} - {e}")
