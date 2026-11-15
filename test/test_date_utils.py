from datetime import date, datetime

import pytest

from src.date_utils import format_date_folder, parse_custom_date


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


def test_parse_custom_date_accepts_valid_date():
    assert parse_custom_date("10-07-2026") == date(2026, 10, 7)


def test_parse_custom_date_rejects_nonexistent_date():
    with pytest.raises(ValueError):
        parse_custom_date("02-30-2026")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("10-07-2026", date(2026, 10, 7)),
        ("10/07/2026", date(2026, 10, 7)),
        ("10.07.26", date(2026, 10, 7)),
        ("100726", date(2026, 10, 7)),
        ("1 7 26", date(2026, 1, 7)),
        ("10/07-2026", date(2026, 10, 7)),
        (" 10-07-2026 ", date(2026, 10, 7)),
        ("10-07-68", date(2068, 10, 7)),
        ("10-07-69", date(1969, 10, 7)),
    ],
)
def test_parse_custom_date_accepts_flexible_formats(value, expected):
    assert parse_custom_date(value) == expected


def test_get_file_dates_returns_creation_and_modification_separately(monkeypatch):
    import src.date_utils as date_utils
    from types import SimpleNamespace

    creation_time = datetime(2026, 10, 7, 12).timestamp()
    modification_time = datetime(2026, 10, 9, 12).timestamp()
    stat_result = SimpleNamespace(
        st_birthtime=creation_time,
        st_ctime=creation_time,
        st_mtime=modification_time,
    )
    monkeypatch.setattr(date_utils.os, "stat", lambda _: stat_result)

    assert date_utils.get_file_dates("sample.pdf") == (
        date(2026, 10, 7),
        date(2026, 10, 9),
    )


def test_get_file_dates_returns_none_when_creation_date_unavailable(monkeypatch):
    import os
    import src.date_utils as date_utils
    from types import SimpleNamespace

    if os.name == "nt":
        pytest.skip("Windows reports st_ctime as the creation time.")

    modification_time = datetime(2026, 10, 9, 12).timestamp()
    stat_result = SimpleNamespace(st_mtime=modification_time)
    monkeypatch.setattr(date_utils.os, "stat", lambda _: stat_result)

    assert date_utils.get_file_dates("sample.pdf") == (
        None,
        date(2026, 10, 9),
    )
