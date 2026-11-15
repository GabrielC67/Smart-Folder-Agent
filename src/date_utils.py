from datetime import date
import re

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
