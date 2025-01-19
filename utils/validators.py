import re
from datetime import datetime
import pandas as pd

def validate_date(date_str: str) -> bool:
    """
    Validates that a string is a valid date in the format YYYY-MM-DD.

    :param date_str: The date string to validate.
    :return: True if the string is a valid date, False otherwise.
    """
    try:
        if pd.isna(date_str):
            return True
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

def validate_numeric(value) -> bool:
    """
    Validates that a value is numeric.

    :param value: The value to validate.
    :return: True if the value is numeric, False otherwise.
    """
    try:
        if pd.isna(value):
            return True
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def validate_boolean(value) -> bool:
    """
    Validates that a value can be interpreted as a boolean (0/1, True/False).

    :param value: The value to validate.
    :return: True if the value is a valid boolean, False otherwise.
    """
    return str(value).lower() in ['0', '1', 'true', 'false']

def sanitize_input(text: str) -> str:
    """
    Sanitizes text input to remove potentially malicious characters.

    :param text: The text to sanitize.
    :return: A sanitized version of the text.
    """
    if pd.isna(text):
        return ''
    return re.sub(r'[<>&;]', '', str(text))

def validate_csv_columns(data: pd.DataFrame, required_columns: set) -> bool:
    """
    Validates that a DataFrame contains the required columns.

    :param data: The DataFrame to validate.
    :param required_columns: A set of required column names.
    :return: True if all required columns are present, False otherwise.
    """
    return required_columns.issubset(data.columns)
