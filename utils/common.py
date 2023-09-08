import inspect
from pathlib import Path
import logging.config
import pytest
import pandas as pd


def get_logger():
    file = logging.FileHandler(
        Path(__file__).parent.parent / "reports/logs/logfile.log"
    )  # File for log
    formatter = logging.Formatter(
        "%(levelname)s :%(name)s :%(message)s :%(asctime)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )  # Format of log
    file.setFormatter(formatter)  # set formatter into file

    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    logger.addHandler(file)  # adding log into file
    logger.setLevel(logging.INFO)
    return logger


def get_test_data(sheet_name):
    excel_path = Path(__file__).parent.parent / "utils/testdata.xlsx"
    df = pd.read_excel(excel_path, sheet_name=sheet_name, dtype=str)
    df_filled = df.fillna("")
    return df_filled.to_dict(orient="records")