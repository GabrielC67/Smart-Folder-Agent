from datetime import datetime
from src.sorter import get_creation_date


def test_extracts_correct_creation_date(tmp_path):
    # 1. Create a temporary dummy file for the test
    test_file = tmp_path / "drone_footage.mp4"
    test_file.write_text("fake video content")

    # 2. Run our (currently non-existent) function
    extracted_date = get_creation_date(str(test_file))

    # 3. Assert it returns a valid datetime object matching today's year
    assert isinstance(extracted_date, datetime)
    assert extracted_date.year == datetime.now().year