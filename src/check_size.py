import os


def main():
    print("=== DJI Storage Calculator ===")
    scan_path = input("Drag and drop your NAS MainPool folder here, then press Enter: ").strip().strip("'").strip('"')

    total_bytes = 0
    count = 0

    print("\n--- Scanning for DJI files ---")
    for root, dirs, files in os.walk(scan_path):
        # Skip Docker system folders to prevent permission errors
        if "appdata" in root.lower() or "compose" in root.lower():
            continue

        for file in files:
            if "DJI" in file.upper():
                filepath = os.path.join(root, file)
                total_bytes += os.path.getsize(filepath)
                count += 1

    total_gb = total_bytes / (1024 * 1024 * 1024)
    print(f"\nFound {count} DJI files.")
    print(f"Total size: {total_gb:.2f} GB")


if __name__ == "__main__":
    main()