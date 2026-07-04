You are an AI assistant helping a technical writer organize a messy collection of legacy documentation.

The writer has provided you with a compressed archive located at `/home/user/legacy_docs.zip`. This archive contains a nested mess of other archives (both `.zip` and `.tar.gz` formats) organized by department, which in turn contain the actual documentation files (`.md` and `.txt`).

Your task is to extract, convert, organize, and catalog these files. Please write and execute a Python script (or use bash commands) to perform the following steps exactly as specified:

1. **Extraction**:
   - Extract `/home/user/legacy_docs.zip` into a new directory: `/home/user/extracted/`.
   - Recursively find and extract all `.zip` and `.tar.gz` files within `/home/user/extracted/` into their respective directories (the contents of the archive should be extracted in the same directory where the archive itself is located).
   - Delete all `.zip` and `.tar.gz` files inside `/home/user/extracted/` after they are extracted.

2. **Format Conversion**:
   - Recursively find all `.txt` files in `/home/user/extracted/`.
   - Convert each `.txt` file to Markdown format. Do this by creating a new `.md` file in the same directory, writing a header line exactly formatted as `# Original File: <filename.txt>\n\n` (where `<filename.txt>` is the original name of the text file), and then appending the original contents of the text file.
   - Delete the original `.txt` files after conversion.

3. **Flattening and Renaming**:
   - Create a directory called `/home/user/final_docs/`.
   - Move every `.md` file from `/home/user/extracted/` (both original and newly converted ones) into `/home/user/final_docs/`.
   - To prevent name collisions, rename the files based on their relative path from `/home/user/extracted/`. Replace all path separators (`/`) with underscores (`_`). 
   - *Example*: If a file was at `/home/user/extracted/engineering/api/auth.md`, it should be moved to `/home/user/final_docs/engineering_api_auth.md`.

4. **Manifest Creation**:
   - Create a JSON file at `/home/user/manifest.json`.
   - This file should contain a single JSON list of strings, representing the absolute file paths of all the files now located in `/home/user/final_docs/`, sorted alphabetically.

Ensure all file paths and exact text formatting requirements are met.