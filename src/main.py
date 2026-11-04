import os


def main():
    print("=== Smart Folder Agent ===")

    # Capture and clean the directory paths from the terminal
    sd_path = input("Drag and drop your SD card folder here, then press Enter: ").strip().strip("'").strip('"')
    pool_path = input("Drag and drop your NAS MainPool folder here, then press Enter: ").strip().strip("'").strip('"')

    print("\n--- Scanning SD Card ---")

    # Traverse the directory
    for root, dirs, files in os.walk(sd_path):
        for file in files:
            # Skip hidden macOS system files to prevent clutter
            if file.startswith("._") or file.startswith("."):
                continue

            filepath = os.path.join(root, file)

            # Placeholder for where we will inject the sorting logic next
            print(f"Discovered valid file: {file}")


if __name__ == "__main__":
    main()