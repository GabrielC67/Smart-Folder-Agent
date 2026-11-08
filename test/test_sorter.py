from datetime import datetime
from src.sorter import get_creation_date
import os
from src.sorter import ensure_directory_exists
from src.sorter import get_category
from src.sorter import determine_document_path
from src.sorter import prompt_user_action
from src.sorter import get_safe_filename
import subprocess
from src.sorter import preview_file

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