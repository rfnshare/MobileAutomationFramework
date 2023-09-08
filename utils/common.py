import inspect
from pathlib import Path
import logging.config
import pytest
import pandas as pd
import glob
import os


def get_logger():
    config_file_path = Path(__file__).parent.parent / 'config/logging.conf'
    # Define a custom log filename
    log_filename = "reports/logs/logfile.log"
    # Check if the log directory exists; if not, create it
    log_directory = os.path.dirname(log_filename)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        print(f"Log File Created in {log_directory}")

    logging.config.fileConfig(config_file_path, defaults={'log_filename': log_filename})
    logger_name = inspect.stack()[1][3]
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
        path = Path(__file__).parent.parent / f'reports/htmlreport/regression_*.html'
        report = os.path.abspath(
            glob.glob(f'{path}')[-1]
        )
        reports.append(report)
    except Exception as e:
        print("Report not ready, Error", e)
    return reports
LOGGING_CONFIG = Path(__file__).parent.parent / 'config/logging.conf'
print(LOGGING_CONFIG)