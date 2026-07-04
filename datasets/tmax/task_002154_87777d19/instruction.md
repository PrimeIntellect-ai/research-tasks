You are acting as a technical writer organizing a messy archive of legacy documentation assets.

A system export dumped various asset files into the `/home/user/legacy_docs/raw_assets` directory. All of the files have meaningless extensions (like `.dat`, `.tmp`, `.bin`) and their original types are lost. 

Your task is to organize these files by inspecting their binary signatures and metadata, and then linking them to a new structured directory.

Here are the exact requirements:
1. **Filter by Metadata:** You only care about files that are strictly greater than 10 Kilobytes (10,240 bytes) in size. Ignore smaller files.
2. **Identify by Binary Header:** For the files that meet the size criteria, inspect their first few bytes (magic numbers) to determine their actual file format. Look for:
   - **PDF:** Starts with `25 50 44 46 2D` (Hex) / `%PDF-` (ASCII)
   - **PNG:** Starts with `89 50 4E 47 0D 0A 1A 0A` (Hex)
   - **JPEG:** Starts with `FF D8 FF` (Hex)
   Ignore files that do not match these headers.
3. **Create Structured Links:** Create a new base directory at `/home/user/organized_docs`. Inside it, create three subdirectories: `pdfs`, `pngs`, and `jpegs`.
4. **Link the Files:** For each valid file found, create a **symbolic link** in the corresponding subdirectory. 
   - The symlink must point to the absolute path of the original file in the `raw_assets` directory.
   - The symlink's name should be the original filename with the correct extension appended (e.g., if `/home/user/legacy_docs/raw_assets/asset_01.dat` is a PDF, the symlink should be `/home/user/organized_docs/pdfs/asset_01.dat.pdf`). Use `.jpg` for JPEGs.
5. **Generate a Log:** Finally, create a log file at `/home/user/organized_docs/summary.txt`. This file must contain a list of all the absolute paths to the *symlinks* you created, sorted alphabetically (one path per line).

You may use any programming language (Python, Bash, etc.) to automate this task.