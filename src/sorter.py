import os
from datetime import datetime
import subprocess


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


def test_prevents_file_collisions():
    # Simulate a file that already exists on the NAS
    existing_file = "REC_001.mp4"

    # Run it through our safe-rename function
    safe_name = get_safe_filename(existing_file)

    # Assert it appends the correct suffix to prevent overwriting
    assert safe_name == "REC_001_SD_Import.mp4"

def get_safe_filename(filename):
    """
    Appends a safe suffix to a filename to prevent overwriting existing files.
    """
    base, ext = os.path.splitext(filename)
    return f"{base}_Organized{ext}"

def prompt_user_action(filename):
    """
    Pauses execution to ask the user what to do with a file.
    Loops until a valid choice is entered.
    """
    print(f"\nFile: {filename}")
    while True:
        choice = input("[M]ove | [P]review | [S]kip: ").strip().lower()

        if choice in ['m', 'p', 's', '']:
            return choice

        print("Invalid input. Please enter M, P, or S.")

def preview_file(filepath):
    """
    Triggers macOS Quick Look for instant video/photo preview.
    """
    # We route stdout and stderr to DEVNULL to keep your terminal clean from qlmanage's verbose logging
    subprocess.run(['qlmanage', '-p', filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def prompt_user_action_folder(folder_name, folder_date):
    """
        Pauses execution when a folder is found and asks the user how to handle it.
        """
    print(f"\nFolder found: {folder_name} (Created: {folder_date})")
    while True:
        print("What would you like to do?")
        print("[1] Move entire folder as-is | [2] Move & organize contents by file type | [S]kip")
        choice = input("Select an option (1, 2, S): ").strip().lower()

        if choice in ['1', '2', 's', '']:
            return choice
        print("Invalid input. Please enter 1, 2, or S.")


def get_custom_folder_name():
    """
    Prompts the user to enter the name of the folder they want to use or create.
    """
    while True:
        folder_name = input("Enter the target folder name (e.g., 'Password Manager Export'): ").strip()
        if folder_name:
            return folder_name
        print("Folder name cannot be empty.")


def get_move_as_is_destination():
    """
    Asks the user where to move a folder as-is.
    """
    while True:
        print("\nWhere would you like to move this folder?")
        print("[A] Existing Folder | [B]New custom folder name | [C] 'Move to Folder Named: Other'")
        choice = input("Select an option (A, B, or C): ").strip().lower()

        if choice == 'a':
            return get_folder_name()
        if choice == 'b':
            return get_custom_folder_name()
        elif choice == 'c':
            return "Other"
        print("Invalid input. Please enter A, B, or C.")


def get_folder_name(pool_path, year, month):
    """
    Scans the Year/Month directory and lets the user pick from a list of existing folders.
    """
    target_dir = os.path.join(pool_path, year, month)

    # Ensure the directory exists so we don't crash trying to list it
    if not os.path.exists(target_dir):
        print(f"\nNo existing folders found in {year}/{month} yet.")
        print("Falling back to creating a new custom folder.")
        return get_custom_folder_name()

    # Get a list of all directories inside this Year/Month
    existing_folders = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]

    if not existing_folders:
        print(f"\nNo existing folders found in {year}/{month} yet.")
        print("Falling back to creating a new custom folder.")
        return get_custom_folder_name()

    # Display the options
    print(f"\nExisting folders in {year}/{month}:")
    for index, folder in enumerate(existing_folders, start=1):
        print(f"[{index}] {folder}")

    while True:
        choice = input(f"Select a folder by number (1-{len(existing_folders)}): ").strip()

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(existing_folders):
                return existing_folders[index - 1]

        print(f"Invalid input. Please enter a number between 1 and {len(existing_folders)}.")