import os
import subprocess
from datetime import datetime
from src.sorter import (get_creation_date, ensure_directory_exists, get_category,
                        determine_document_path, prompt_user_action, get_safe_filename, preview_file,
                        prompt_user_action_folder, get_move_as_is_destination, get_folder_name)



def test_extracts_correct_creation_date(tmp_path):
    # 1. Create a temporary dummy file for the test
    test_file = tmp_path / "drone_footage.mp4"
    test_file.write_text("fake video content")

    # 2. Run our (currently non-existent) function
    extracted_date = get_creation_date(str(test_file))

    # 3. Assert it returns a valid datetime object matching today's year
    assert isinstance(extracted_date, datetime)
    assert extracted_date.year == datetime.now().year


def test_creates_directory_if_missing(tmp_path):
    # Define a test path inside our safe temporary directory
    target_dir = tmp_path / "2026" / "10_October"

    # Run the function
    ensure_directory_exists(str(target_dir))

    # Assert the folder was actually created on the OS level
    assert target_dir.exists()
    assert target_dir.is_dir()

def test_identifies_correct_media_categories():
    # Test video routing
    assert get_category("drone_footage.mp4") == "Videos"
    assert get_category("dashcam.MOV") == "Videos"

    # Test picture routing
    assert get_category("vacation.jpg") == "Pictures"
    assert get_category("screenshot.PNG") == "Pictures"

    # Test document routing
    assert get_category("taxes.pdf") == "Documents"
    assert get_category("notes.docx") == "Documents"


def test_prevents_file_collisions():
    # Simulate a file that already exists on the NAS
    existing_file = "REC_001.mp4"

    # Run it through our safe-rename function
    safe_name = get_safe_filename(existing_file)

    # Assert it appends the correct suffix to prevent overwriting
    assert safe_name == "REC_001_Organized.mp4"

def test_existing_document_folders():
    organized_doc = "Social Security/card_scan.pdf"
    assert determine_document_path(organized_doc, "Documents") == "Documents/Social Security"

def test_nonexisting_document_folders():
    unorganized_doc = "taxes.pdf"
    assert determine_document_path(unorganized_doc, "Documents") == "Documents"


def test_interactive_prompt(monkeypatch):
    # Simulate a user typing 'm' and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: 'm')

    # Run the prompt function for a dummy file
    choice = prompt_user_action("REC_001.mp4")

    # Assert it correctly captures and returns the 'm' keystroke
    assert choice == 'm'


def test_preview_triggers_macos_system_player(monkeypatch):
    # 1. Create a list to capture the system command our script tries to run
    captured_command = []

    def mock_subprocess_run(command, **kwargs):
        captured_command.append(command)

    # 2. Intercept the real subprocess.run and replace it with our safe mock
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)

    # 3. Run the function
    preview_file("drone_footage.mp4")

    # 4. Assert it actually tried to execute a command on the target file
    assert len(captured_command) == 1
    assert "drone_footage.mp4" in captured_command[0]

def test_folder_action_prompt_returns_valid_choice(monkeypatch):
    # Simulate the user typing '2' (Move & organize contents) and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: '2')

    # Run the prompt function for a dummy folder and date
    choice = prompt_user_action_folder("Password Manager Export", "2026/10_October")

    # Assert it correctly captures and returns the '2' keystroke
    assert choice == '2'

def test_get_move_as_is_destination_returns_others(monkeypatch):
    # Simulate the user typing 'b' (for 'Other') and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: 'c')

    #Run the prompt function
    destination = get_move_as_is_destination()

    #Assert it correctly returns "Other"
    assert destination == "Other"


def test_other_directory_creation_does_not_duplicate(tmp_path):
    # Simulate a Year/Month base directory
    year_month_dir = tmp_path / "2026" / "10_October"
    other_dir = year_month_dir / "Other"

    # Run ensure_directory_exists twice to simulate multiple files choosing C
    ensure_directory_exists(str(other_dir))
    ensure_directory_exists(str(other_dir))

    # Assert the directory exists and only one 'Other' folder was created without error
    assert other_dir.exists()
    assert other_dir.is_dir()


def test_get_move_as_is_destination_returns_a(monkeypatch):
    folder_name = "get_folder_name"
    # Simulate the user typing 'a' (for existing folder) and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: 'a')

    # Mock get_folder_name so the test doesn't freeze waiting for the second input
    import src.sorter
    monkeypatch.setattr(src.sorter, folder_name, lambda: 'Existing Folder Name')

    # Run the prompt function
    destination = get_move_as_is_destination()

    # Assert it correctly returns the mocked existing folder name
    assert destination == "Existing Folder Name"


def test_get_folder_name_displays_existing_directories(monkeypatch, tmp_path, capsys):
    # Set up a dummy NAS MainPool directory structure
    pool = tmp_path / "MainPool"
    year_month = pool / "2026" / "10_October"

    # Create some dummy folders inside that Year/Month to populate the list
    (year_month / "Social Security").mkdir(parents=True)
    (year_month / "Work related").mkdir()
    (year_month / "Court information").mkdir()

    # Simulate the user selecting option '2' from the list
    monkeypatch.setattr('builtins.input', lambda _: '2')

    # Run the function passing our dummy paths
    selected = get_folder_name(str(pool), "2026", "10_October")

    # Capture the terminal output to verify the numbered list was displayed
    captured = capsys.readouterr()

    # Assertions
    assert "Existing folders in 2026/10_October:" in captured.out
    assert "[1]" in captured.out
    assert "[2]" in captured.out
    assert "[3]" in captured.out

    # Assert it correctly returned the selected folder
    assert selected in ["Social Security", "Work related", "Court information"]


def test_get_custom_folder_name_returns_input(monkeypatch):
    # Simulate the user typing 'New Tax Folder' and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: 'New Tax Folder')

    # Run the function
    from src.sorter import get_custom_folder_name
    folder_name = get_custom_folder_name()

    # Assert it correctly returns what the user typed
    assert folder_name == "New Tax Folder"