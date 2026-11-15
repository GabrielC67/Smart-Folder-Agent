import os
import re
from datetime import date, datetime
from typing import Optional

MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)

def format_date_folder(value: date) -> str:
    day = value.day
    if 11 <= day % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    month = MONTH_NAMES[value.month - 1]
    return f"{month} {day}{suffix}, {value.year}"


def parse_custom_date(value: str) -> date:
    value = value.strip()
    match = re.fullmatch(r"([0-9]{2})([0-9]{2})([0-9]{4}|[0-9]{2})", value)
    if match is None:
        match = re.fullmatch(
            r"([0-9]{1,2})[./ -]+([0-9]{1,2})[./ -]+([0-9]{4}|[0-9]{2})",
            value,
        )
    if match is None:
        raise ValueError("Enter a date in month-day-year order.")

    month, day, year = match.groups()
    year_number = int(year)
    if len(year) == 2:
        year_number += 2000 if year_number <= 68 else 1900

    return date(year_number, int(month), int(day))


def get_file_dates(filepath: str) -> tuple[Optional[date], date]:
    stat = os.stat(filepath)

    creation_timestamp = getattr(stat, "st_birthtime", None)
    if creation_timestamp is None and os.name == "nt":
        creation_timestamp = stat.st_ctime

    creation_date = (
        datetime.fromtimestamp(creation_timestamp).date()
        if creation_timestamp is not None
        else None
    )
    modification_date = datetime.fromtimestamp(stat.st_mtime).date()
    return creation_date, modification_date
