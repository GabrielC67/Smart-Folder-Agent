from datetime import date

import pytest

from src.date_utils import format_date_folder


@pytest.mark.parametrize(
    ("day", "expected"),
    [
        (1, "October 1st, 2026"),
        (2, "October 2nd, 2026"),
        (3, "October 3rd, 2026"),
        (4, "October 4th, 2026"),
        (11, "October 11th, 2026"),
        (12, "October 12th, 2026"),
        (13, "October 13th, 2026"),
        (21, "October 21st, 2026"),
        (22, "October 22nd, 2026"),
        (23, "October 23rd, 2026"),
        (31, "October 31st, 2026"),
    ],
)
def test_formats_date_folder_with_ordinal_day(day, expected):
    assert format_date_folder(date(2026, 10, day)) == expected


def test_formats_another_month():
    assert format_date_folder(date(2026, 2, 1)) == "February 1st, 2026"
