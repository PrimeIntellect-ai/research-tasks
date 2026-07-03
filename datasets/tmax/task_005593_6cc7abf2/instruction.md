You need to build a C-based configuration change tracker that detects updates in JSON configuration files and maintains state in a binary file.

System State & Requirements:
1. There is a binary state file located at `/home/user/state.bin`. This file contains an array of records representing the last known configuration versions of various applications.
   Each record is exactly 36 bytes, structured as:
   - `app_name`: 32 bytes (null-terminated string, ASCII).
   - `version`: 4 bytes (32-bit signed integer, little-endian).
2. There is a directory `/home/user/configs/` containing several `.json` files.
3. Each JSON file contains configuration data, including an `"app_name"` (string) and a `"config_version"` (integer). Example: `{"app_name": "db_backend", "config_version": 2, "max_connections": 100}`.

Your tasks:
1. Write a C program at `/home/user/tracker.c`. You may use standard libraries and install `libjson-c-dev` via the package manager to parse JSON.
2. The program must:
   - Read `/home/user/state.bin` into memory.
   - Iterate through all `.json` files in `/home/user/configs/`.
   - Parse each JSON file to extract `app_name` and `config_version`.
   - Compare the parsed version against the version in the binary state:
     - If the application exists in the state file and the JSON `config_version` is *strictly greater* than the state version, register an update.
     - If the application does *not* exist in the state file, register it as a new application (treat the old version as `0`).
     - If the application exists but the JSON version is equal or lower, do nothing.
   - For every update or new application, output a line to standard output (stdout) in the format: `app_name,old_version,new_version`.
   - The output lines must be sorted alphabetically by `app_name`.
   - Update the state records in memory with the new versions (and append any new applications). Existing applications not present in the JSON files must remain in the state file untouched.
   - Write the entire updated state back to `/home/user/state.bin`, preserving the exact 36-byte binary format per record.
3. Compile your program to `/home/user/tracker`.
4. Run your program and redirect its standard output to `/home/user/updates.csv`.

Verify your implementation by checking that `/home/user/updates.csv` contains the correct CSV data and that `/home/user/state.bin` has been correctly updated.