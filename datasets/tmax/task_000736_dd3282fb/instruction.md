You are tasked with organizing a large legacy project's files. The project contains thousands of data files with obscure binary headers. 

Historically, developers used a proprietary, compiled tool located at `/app/legacy_categorizer` to read these files and determine their correct project categorization. However, this binary is deprecated, extremely slow, and we are migrating to a new architecture. 

Your objectives are:
1. **Reverse-Engineer the Binary**: Analyze what `/app/legacy_categorizer` does. It takes a single file path as an argument and outputs a JSON string containing metadata extracted from the file's binary header (e.g., `{"project_id": 42, "file_type": "log", "timestamp": 1610000000}`).
2. **Implement a Python Parser**: Write a highly optimized Python script at `/home/user/parser.py`. This script must accept a directory path as a command-line argument, parse all `.dat` files within it directly in Python (without calling the legacy binary), and output a single file `metadata_report.json` in the current directory mapping filenames to their extracted metadata.
3. **Bulk Organization**: Write a second script `/home/user/organize.py` that reads a configuration file `/home/user/organization_rules.json` (which maps `project_id` and `file_type` to specific folder structures) and uses your `parser.py` logic to bulk-rename and move all files from `/home/user/legacy_data/` into a new directory `/home/user/organized_data/`.

**Constraints:**
- `/app/legacy_categorizer` is a stripped binary. You will need to create some dummy binary files, run them through the tool, and deduce the header format (hint: it's a fixed-size header at the very beginning of the file, involving basic integer types and a simple bitwise operation).
- `parser.py` must be fast and completely standalone.
- The automated test will run your `parser.py` on a held-out dataset of 50,000 files to measure its accuracy. Your script must process them and achieve a perfect metadata extraction score.

Please write the scripts and perform the initial organization on `/home/user/legacy_data/`.