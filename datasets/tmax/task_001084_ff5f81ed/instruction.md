I am migrating an old legacy project from Python 2 to Python 3. Our codebase has a strict integrity checking step because we frequently encountered conflicting peer dependencies and corrupted script downloads in our old build process. 

I have a directory at `/home/user/legacy_project` that contains a `checksums.md5` file and a `src/` directory with several Python scripts. 

I need you to identify exactly which scripts need to be migrated because they use the Python 2 `print` statement. However, due to previous corrupted downloads in this environment, you must **only** consider files that pass the MD5 checksum verification. 

Write a bash command or short script that:
1. Validates the files in `/home/user/legacy_project/src/` against `/home/user/legacy_project/checksums.md5`.
2. For the files that pass the checksum (are reported as "OK"), checks if they contain a Python 2 style print statement. For this task, define a Python 2 print statement strictly as a line that matches the extended regular expression `^[[:space:]]*print[[:space:]]+["']` (i.e., the word `print` followed by at least one space, followed immediately by a single or double quote, ignoring leading indentation).
3. Outputs the relative paths (e.g., `src/filename.py`) of the files that satisfy **both** constraints (checksum passes AND contains Python 2 print).
4. Saves this list to `/home/user/migration_targets.txt`, with one file path per line, sorted alphabetically.

Do not modify the original Python files or the checksum file. Use standard bash tools (like `md5sum`, `grep`, `awk`, etc.) to generate the output file.