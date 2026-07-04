You are tasked with recovering and parsing a corrupted configuration backup directory. A legacy configuration management tool has created a complex directory structure at `/home/user/config_tree`. Unfortunately, poor link management has resulted in several symbolic links that form infinite loops. 

Your goal is to write a purely Bash-based script (using standard CLI tools like `find`, `awk`, `sed`, `od`, `hexdump`, etc.) that traverses this directory, safely identifies and logs the symlink loops, and extracts configuration metadata from both text and proprietary binary configuration files into a consolidated CSV report.

**Task Requirements:**

1. **Symlink Loop Detection:**
   During your recursive traversal of `/home/user/config_tree`, you must identify any symbolic links that result in infinite loops. 
   - Write the absolute path of every looping symlink to `/home/user/loops.log`, one per line, sorted alphabetically. 
   - You must skip these loops to prevent your script from hanging.
   - Ignore standard broken symlinks (symlinks pointing to non-existent files that aren't loops); only log the ones that form infinite recursive loops.

2. **Configuration Extraction:**
   Parse all valid, non-looping regular files in the directory tree. There are two types of configuration files you need to process. You must determine the type by inspecting the file, not just relying on extensions:
   
   *Type A: Text Configurations*
   - These files contain `key=value` pairs.
   - Ignore empty lines and lines starting with `#`.
   - Extract the values for the keys `app_name` and `version` (keys are case-insensitive).
   
   *Type B: Binary Configurations*
   - These files begin with a specific 4-byte magic signature: `0x42 0x43 0x46 0x47` (ASCII "BCFG").
   - The 5th byte (offset 4) is a single-byte unsigned integer representing the `version`.
   - Starting from the 6th byte (offset 5) is a null-terminated ASCII string representing the `app_name`.

3. **Consolidated CSV Report:**
   - Generate a report at `/home/user/report.csv`.
   - The CSV must have the following header: `filepath,type,app_name,version`
   - `filepath` must be the absolute path to the resolved configuration file.
   - `type` must be either `TEXT` or `BINARY`.
   - `app_name` and `version` are the extracted values.
   - Sort the CSV rows alphabetically by `filepath` (ignoring the header row, which should remain at the top).

Constraints:
- Use only Bash and standard Unix tools (e.g., `awk`, `sed`, `grep`, `find`, `hexdump`, `od`). Do not use Python, Perl, or other scripting languages.
- You must create a script, run it, and ensure both `/home/user/loops.log` and `/home/user/report.csv` are accurately generated.