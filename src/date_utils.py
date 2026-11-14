from datetime import date

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
