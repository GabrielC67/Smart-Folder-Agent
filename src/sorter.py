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

def ensure_directory_exists(dir_path):
    """
    Creates the target directory if it does not already exist.
    """
    os.makedirs(dir_path, exist_ok=True)


def get_category(filename):
    """
    Categorizes a file based on its extension.
    """
    # Extract the extension and convert to lowercase (e.g., '.JPG' becomes '.jpg')
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.heic']:
        return "Pictures"
    elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
        return "Videos"
    elif ext in ['.pdf', '.doc', '.docx', '.txt']:
        return "Documents"

    return "Unknown"


def determine_document_path(filename, base_category):
    """
    Handles routing for documents, preserving existing sub-directories.
    """
    # If the filename contains a slash, it means it's already inside a folder
    if "/" in filename:
        # Split the path into the folder name and the actual file
        folder_name, _ = os.path.split(filename)
        return f"{base_category}/{folder_name}"

    # If it's a loose file, just return the base category (e.g., 'Documents')
    return base_category
