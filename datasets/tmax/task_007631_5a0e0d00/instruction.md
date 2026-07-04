I have a very disorganized project directory located at `/home/user/messy_project`. It contains a mix of Python source files and text notes scattered across many nested folders. 

I need you to help me organize these files by performing the following operations using standard Linux commands:

1. **Bulk Rename**: Find all `.txt` files recursively in `/home/user/messy_project` that contain the exact string `TODO` (case-sensitive) anywhere in their contents. Rename these specific files so their extension is `.todo` instead of `.txt`. Leave other `.txt` files untouched.

2. **Merge**: Find all Python files (`*.py`) recursively in `/home/user/messy_project`. Concatenate all of their contents into a single new file located at `/home/user/all_code.py`. The files must be concatenated in alphabetical order based on their absolute file paths.

3. **Chunking**: Take the newly created `/home/user/all_code.py` and split it into smaller files of exactly 50 lines each (the final file may have fewer than 50 lines). Place these chunked files in a new directory called `/home/user/chunks/`. Name the output files with the prefix `chunk_`, a 2-digit numeric suffix starting at `00`, and the extension `.py` (e.g., `chunk_00.py`, `chunk_01.py`).

Please execute the commands to achieve this exact final state.