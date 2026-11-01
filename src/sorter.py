import os
from datetime import datetime


def get_creation_date(filepath):
    """
    Extracts the creation date of a file.
    Falls back to modification date if creation date is unavailable.
    """
    # macOS/Linux typically expose creation time via st_birthtime or st_ctime
    stat = os.stat(filepath)
    try:
        timestamp = stat.st_birthtime
    except AttributeError:
        timestamp = stat.st_mtime

    return datetime.fromtimestamp(timestamp)