I need you to help me organize some scattered Python project files into a single consolidated source directory and then safely archive them. 

I have a directory at `/home/user/projects_raw/` that contains various files (like `.py`, `.md`, `.txt`) nested inside several subdirectories.

Please write and execute a Python script at `/home/user/organize.py` that does the following:
1. Recursively traverses `/home/user/projects_raw/` to find all `.py` files.
2. Copies all the discovered `.py` files into a single flat directory at `/home/user/organized_src/` (create this directory if it doesn't exist).
3. As you copy them, rename each file by prepending `src_` to its original filename (e.g., `main.py` becomes `src_main.py`). You can assume all original `.py` filenames are unique across the entire directory tree.
4. After copying and renaming the files, create a `.tar.gz` archive of the `/home/user/organized_src/` directory. 
5. To ensure the archive isn't corrupted if the script is interrupted, you must first write the archive to a temporary file using Python's `tempfile` module, and then atomically move (or replace) it to the final destination at `/home/user/src_archive.tar.gz`.

Ensure your script handles everything end-to-end and execute it.