You are an AI assistant helping a technical writer organize a large, messy dump of documentation archives. You need to write and execute a Bash script to process these files, verifying their integrity, extracting them, finding specific files based on metadata, and organizing them using links to save disk space.

Here are your instructions:

1. **Working Directories**: 
   All your operations should start from `/home/user/incoming_docs/`. This directory contains several `.tar.gz` and `.zip` archive files.

2. **Archive Integrity & Extraction**:
   Write a Bash script at `/home/user/organize_docs.sh`. When executed, this script must:
   - Create the directories `/home/user/quarantine/` and `/home/user/extracted/`.
   - Test the integrity of every `.tar.gz` and `.zip` file in `/home/user/incoming_docs/`.
   - If an archive is corrupted or invalid, move it to `/home/user/quarantine/`.
   - If an archive is valid, extract its contents entirely into `/home/user/extracted/`. Maintain the directory structure from the archives during extraction.

3. **Metadata-Based Search & Link Management**:
   After extraction, your script must:
   - Create the directories `/home/user/recent_docs/hardlinks/` and `/home/user/recent_docs/symlinks/`.
   - Search through `/home/user/extracted/` (and all its subdirectories) for all Markdown files (`*.md`) that were last modified **on or after January 1, 2023** (specifically, 2023-01-01 00:00:00 or newer).
   - For every matching `.md` file found, create a **hard link** in `/home/user/recent_docs/hardlinks/` with the exact same filename. (Assume filenames are unique for this task).
   - For every matching `.md` file found, create a **symbolic link** (symlink) in `/home/user/recent_docs/symlinks/` with the exact same filename. The symlink must point to the absolute path of the extracted file inside `/home/user/extracted/`.

4. **Summary Log**:
   Finally, your script must generate a log file at `/home/user/summary.log` with exactly three lines:
   - Line 1: The integer count of corrupted archives moved to quarantine.
   - Line 2: The integer count of valid archives extracted.
   - Line 3: The integer count of recent `.md` files linked.

Run your script to complete the task. Do not assume any pre-existing aliases; use standard bash tools (like `find`, `tar`, `unzip`, `ln`, `gzip`).