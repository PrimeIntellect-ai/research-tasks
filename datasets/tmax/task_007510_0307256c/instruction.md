You are tasked with helping a developer organize a messy legacy project directory located at `/home/user/project_dump`.

The directory contains various nested folders with `.txt` files. Over the years, these files have been saved in different character encodings (such as ISO-8859-1, Windows-1252, Shift-JIS, etc.), and there are many exact duplicates scattered around. Furthermore, a legacy background job still accesses these files periodically.

Write and execute a Python script (`/home/user/organizer.py`) that performs the following tasks:
1. **Recursive Traversal:** Traverse `/home/user/project_dump` recursively to find all `.txt` files.
2. **Encoding Conversion:** Detect the encoding of each `.txt` file and convert its contents to `UTF-8`. Save the UTF-8 content back to the same file. 
3. **Concurrent Access Safety:** Because a background process might be reading or writing to these files, your Python script MUST acquire an exclusive file lock (using `fcntl.flock`) on each file before reading and writing to it, and release it afterward.
4. **Hard Link Deduplication:** After converting to UTF-8, identify files that have the exact same content. Keep the first one you process as the primary file, and replace all subsequent identical files with a **hard link** to the primary file to save disk space.
5. **Symbolic Links for Readmes:** For any file named `readme.txt` (case-insensitive, e.g., `Readme.TXT`, `readme.txt`), create a symbolic link named `README.md` in the exact same directory, pointing to the `readme.txt` file.

Once your script finishes executing, generate a report file at `/home/user/report.txt` containing the total number of `.txt` files processed on the first line, and the number of hard links created for deduplication on the second line.

Do not delete any directories or non-text files. Use standard library modules or install necessary packages (like `chardet` or `charset-normalizer`) if needed.