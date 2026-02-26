"""Class to model the record of a monitoring check, containing the URL and the response time."""

import re
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from backend.src.services.monitor.models.url import URL


def validate_date_format(date_as_str: str) -> str:
    """Validator to check whether the date is in the expected format

    Args:
        date_as_str (str): _description_

    Returns:
        str: date_as_str if the validation succeeds
    """
    # note: below regex does not support i18n, as this is in english.
    # also this is a very basic validator, because it does not consider
    # the different number of days in each month, leap years, etc.
    # However, it is a good approximation for the expected format.
    date_format = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([0-2][0-9]|3[0-1]) ([0-9]{4})'
    if not re.match(date_format, date_as_str):
        raise ValueError(f"Date {date_as_str} is in an invalid format.")
    return date_as_str

def validate_time_format(time_as_str: str) -> str:
    """Validator to check whether the time is in the expected format
    
    Args:
        date_as_str (str): _description_

    Returns:
        str: date_as_str if the validation succeeds
    """
    time_format = r'^(([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])'
    if not re.match(time_format, time_as_str):
        raise ValueError(f"Time {time_as_str} is in an invalid format.")
    return time_as_str

def validate_weekday_format(weekday_as_str: str) -> str:
    """Validator to check whether the weekday is in the expected format

    Args:
        date_as_str (str): _description_

    Returns:
        str: date_as_str if the validation succeeds
    """
    weekday_format = r'Mon|Tue|Wed|Thu|Fri|Sat|Sun'
    if not re.match(weekday_format, weekday_as_str):
        raise ValueError(f"Weekday {weekday_as_str} is in an invalid format.")
    return weekday_as_str

class MonitorRecord(BaseModel):
    """Class to model a monitoring record, grouping an URL and its response time with the measured date/time"""
    url: URL
    response_time: float
    date: Annotated[str, AfterValidator(validate_date_format)]
    time: Annotated[str, AfterValidator(validate_time_format)]
    weekday: Annotated[str, AfterValidator(validate_weekday_format)]
