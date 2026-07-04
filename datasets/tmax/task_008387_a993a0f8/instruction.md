You are tasked with building a configuration management tracker in C++ that processes a Write-Ahead Log (WAL) of configuration changes, parses structured configuration files, generates a state manifest, and archives the active configuration files.

The system state is located in `/home/user/config_data/`. This directory contains:
1. `history.wal`: A domain-specific Write-Ahead Log tracking changes to configuration files. 
2. Several JSON configuration files (e.g., `app1.json`, `app2.json`, etc.).

The `history.wal` file format is a plain text file where each line represents an operation, separated by spaces:
`[SEQUENCE_ID] [OPERATION] [FILENAME]`
Example:
`001 ADD web_server.json`
`002 UPDATE web_server.json`
`003 DELETE old_cache.json`

Valid operations are `ADD`, `UPDATE`, and `DELETE`. A file is considered "active" if its last operation in the WAL is `ADD` or `UPDATE`. If the last operation for a file is `DELETE`, it is no longer active.

Your objective is to write a C++ program (save it as `/home/user/config_tracker.cpp`) that performs the following tasks:
1. Parse `/home/user/config_data/history.wal` to determine the set of currently active configuration files.
2. For each active file, parse the corresponding JSON file in `/home/user/config_data/` to extract the value of the `"version"` key. The JSON files are simple and flat; you may use standard string manipulation or regex if you prefer not to install external JSON libraries.
3. Compute the SHA256 checksum of each active file. You may use shell commands like `sha256sum` via C++ `popen()` or similar mechanisms.
4. Output a manifest file to `/home/user/output/manifest.csv`.
5. Create a compressed tarball of ONLY the active configuration files at `/home/user/output/active_configs.tar.gz`.

Requirements for `/home/user/output/manifest.csv`:
- It must include a header line exactly as: `filename,version,sha256`
- Each subsequent line must detail an active file, sorted alphabetically by filename.
- The `sha256` column should contain only the 64-character hash.

Requirements for `/home/user/output/active_configs.tar.gz`:
- It must be a valid gzip-compressed tar archive.
- It must contain only the active JSON files. Do not include the WAL file, deleted files, or parent directory structures (e.g., extracting it should yield `app1.json` directly, not `home/user/config_data/app1.json`).

Compile your C++ program using `g++ -std=c++17 /home/user/config_tracker.cpp -o /home/user/config_tracker` and execute it to generate the required outputs. Create the `/home/user/output/` directory if it does not exist.