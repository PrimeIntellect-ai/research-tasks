You are acting as a configuration manager. You have inherited a directory of fragmented, legacy configuration files that need to be cleaned, sanitized, and consolidated into a single tracking format.

The messy configurations are located in `/home/user/config_backups/`.
You must perform a multi-phase operation to standardize these files using Bash utilities and Python.

**Phase 1: File Merging and Bulk Renaming**
1. Some configurations are split into multiple parts (e.g., `app_server.part1.cfg`, `app_server.part2.cfg`). You must merge all files that share the same base name and have `.partX.` in their name into a single file named `<basename>.cfg` (e.g., `app_server.cfg`). Merge them in numerical order of their part number. Delete the original part files after merging.
2. Some files have a `.txt` extension but are actually INI configuration files. Any file in the directory with a `.txt` extension that contains at least one INI section header (e.g., `[section_name]`) must be renamed to have a `.ini` extension.

**Phase 2: Text Transformation and Sanitization**
Security policy requires that we track and redact secrets before parsing.
1. Scan all `.cfg` and `.ini` files in `/home/user/config_backups/`.
2. Find any lines starting with `password=` or `api_key=` (case-insensitive, ignoring leading whitespace).
3. Replace the actual value with the exact string `REDACTED`.
4. For every redaction made, append a record to `/home/user/redaction_audit.log` in the exact format: `<filename>:<line_number>:<matched_key>`.
   Example: `app_server.cfg:14:password`
   (Note: Use just the filename, not the full path, in the log).

**Phase 3: Format Conversion and Atomic Writing**
Write a Python script `/home/user/consolidate.py` that reads the sanitized `.cfg` and `.ini` files and converts them into a single master JSON file.
1. `.ini` files should be parsed as nested dictionaries (Section -> Key -> Value).
2. `.cfg` files should be parsed as flat dictionaries of Key -> Value (ignoring blank lines and lines starting with `#`).
3. The final JSON structure must be a dictionary where the top-level keys are the filenames (e.g., `app_server.cfg`, `db_config.ini`), and the values are their parsed dictionaries.
4. **Atomic Write:** The Python script MUST write the JSON data to a temporary file named `/home/user/master_config.json.tmp` first, and then atomically rename it to `/home/user/master_config.json` to prevent partial writes. Ensure the JSON is formatted with an indentation of 2 spaces.

Run your script to produce the final `/home/user/master_config.json`.