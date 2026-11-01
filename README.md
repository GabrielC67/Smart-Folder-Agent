# Smart Folder Agent

An interactive, human-in-the-loop Python utility designed to safely triage, organize, and migrate files across a Raspberry Pi NAS running MergerFS. 

## Core Features
Instead of blindly moving network files and causing data loss, this agent runs locally and relies on an interactive dry-run review process. It uses strict metadata rules to build a predictable, date-driven archive:

* **Date Extraction:** Scans file metadata to determine the exact creation date[cite: 7].
* **Year & Month Hierarchy:** Automatically generates a top-level Year folder, followed by a Month subfolder[cite: 7].
* **Smart Sorting:**
  * **Media Files (.jpg, .mp4, etc.):** Automatically routed into either a `Pictures` or `Videos` subfolder, with optional grouping by location[cite: 7].
  * **Unsorted Documents:** Loose documents are moved into a general `Documents` folder under the corresponding month[cite: 7].
  * **Pre-Organized Documents:** If a document is already inside a specific named folder (e.g., "Social Security"), the entire folder structure is preserved intact under that month's `Documents` directory[cite: 7].

## Testing
This project uses `pytest` to simulate file movements and ensure correct folder path generation before executing any SMB network transfers.