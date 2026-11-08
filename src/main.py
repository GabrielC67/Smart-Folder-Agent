import os
import shutil
from src.sorter import (
    get_creation_date, get_category, determine_document_path,
    ensure_directory_exists, get_safe_filename, prompt_user_action, preview_file
)


def main():
    print("=== Smart Folder Agent: NAS Internal Organizer ===")

    pool_path = input("Drag and drop your NAS MainPool folder here, then press Enter: ").strip().strip("'").strip('"')

    print("\n--- Scanning MainPool ---")

    for root, dirs, files in os.walk(pool_path):
        # Skip Docker system folders to prevent breaking containers
        if "appdata" in root.lower() or "compose" in root.lower():
            continue

        for file in files:
            if file.startswith("._") or file.startswith("."):
                continue

            filepath = os.path.join(root, file)

            # 1. Extract Date & Build Folders
            try:
                creation_date = get_creation_date(filepath)
                year = creation_date.strftime("%Y")
                month = creation_date.strftime("%m_%B")
            except Exception:
                continue  # Skip if date metadata is missing

            # 2. Determine Category
            category = get_category(file)

            # 3. Preserve Document Sub-Folders
            if category == "Documents":
                rel_path = os.path.relpath(filepath, pool_path)
                category_path = determine_document_path(rel_path, "Documents")
            else:
                category_path = category

            # 4. Construct exact destination
            dest_dir = os.path.join(pool_path, year, month, category_path)
            dest_filepath = os.path.join(dest_dir, file)

            # Skip if the file is already organized in its correct destination
            if filepath == dest_filepath:
                continue

            # 5. Interactive Loop
            while True:
                print(f"\nFound: {file} at {root}")
                print(f"Plan: Move to -> {dest_dir}")
                choice = prompt_user_action(file)

                if choice == 'p':
                    preview_file(filepath)
                elif choice == 'm':
                    ensure_directory_exists(dest_dir)
                    if os.path.exists(dest_filepath):
                        safe_name = get_safe_filename(file)
                        dest_filepath = os.path.join(dest_dir, safe_name)

                    shutil.move(filepath, dest_filepath)
                    print(f"Moved -> {dest_filepath}")
                    break
                elif choice in ['s', '']:
                    print("Skipped.")
                    break


if __name__ == "__main__":
    main()