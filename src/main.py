import os
from src.sorter import get_creation_date, get_category, determine_document_path


def main():
    print("=== Smart Folder Agent ===")

    sd_path = input("Drag and drop your SD card folder here, then press Enter: ").strip().strip("'").strip('"')
    pool_path = input("Drag and drop your NAS MainPool folder here, then press Enter: ").strip().strip("'").strip('"')

    print("\n--- Scanning SD Card ---")

    for root, dirs, files in os.walk(sd_path):
        for file in files:
            if file.startswith("._") or file.startswith("."):
                continue

            filepath = os.path.join(root, file)

            # 1. Extract Date & Build Top-Level Folders
            creation_date = get_creation_date(filepath)
            year = creation_date.strftime("%Y")
            month = creation_date.strftime("%m_%B")

            # 2. Determine Category
            category = get_category(file)

            # 3. Preserve Document Sub-Folders
            if category == "Documents":
                # Get the file's path relative to the SD card to check for existing folders
                rel_path = os.path.relpath(filepath, sd_path)
                category_path = determine_document_path(rel_path, "Documents")
            else:
                category_path = category

            # 4. Construct the exact planned destination directory
            dest_dir = os.path.join(pool_path, year, month, category_path)

            print(f"Plan: {file} -> {dest_dir}")


if __name__ == "__main__":
    main()