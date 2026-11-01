from datetime import datetime
from src.sorter import get_creation_date
import os
from src.sorter import ensure_directory_exists
from src.sorter import get_category
from src.sorter import determine_document_path
from src.sorter import get_safe_filename

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

def test_existing_document_folders():
    organized_doc = "Social Security/card_scan.pdf"
    assert determine_document_path(organized_doc, "Documents") == "Documents/Social Security"

def test_nonexisting_document_folders():
    unorganized_doc = "taxes.pdf"
    assert determine_document_path(unorganized_doc, "Documents") == "Documents"

    