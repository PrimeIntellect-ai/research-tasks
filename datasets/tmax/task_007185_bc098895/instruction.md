You are tasked with analyzing historical configuration backups to track version drift across our server fleet. As the Configuration Manager, you need to extract specific configuration states from a massive archive of custom binary configuration files.

The configuration backups are stored recursively in `/home/user/config_backups/`. Each subdirectory represents a server (e.g., `/home/user/config_backups/db-server/`, `/home/user/config_backups/web-server/`). 

The backups are stored in a custom binary format called `CCF` (Custom Config Format). Some files are raw (`.ccf`) and some are gzip-compressed (`.ccf.gz`). 

Your objective is to write a Python script that traverses the backup directory, parses the binary files, extracts the `target_version` key for each server, and safely writes the latest state to a summary file.

### CCF Binary Format Specification:
All integers are Little-Endian. Strings are UTF-8 encoded and not null-terminated.
1. **Header:**
   - Magic Bytes (4 bytes): `0x43 0x43 0x46 0x31` (ASCII "CCF1")
   - Timestamp (4 bytes): Unsigned 32-bit integer representing the Unix timestamp of the backup.
   - Entry Count (2 bytes): Unsigned 16-bit integer representing the number of configuration key-value pairs.
2. **Entries (Repeated `Entry Count` times):**
   - Key Length (2 bytes): Unsigned 16-bit integer.
   - Key (Variable length): UTF-8 string of `Key Length` bytes.
   - Value Length (4 bytes): Unsigned 32-bit integer.
   - Value (Variable length): UTF-8 string of `Value Length` bytes.

### Requirements:
1. **Directory Traversal**: Recursively search `/home/user/config_backups/` for `.ccf` and `.ccf.gz` files.
2. **I/O & Parsing**: 
   - For raw `.ccf` files, use `mmap` (memory-mapped file I/O) to read and parse the files efficiently.
   - For `.ccf.gz` files, stream the decompression using the `gzip` module.
3. **Verification**: Some files are corrupted or do not start with the correct "CCF1" magic bytes. Your code must handle `gzip.BadGzipFile` exceptions and verify the magic bytes. Skip any invalid or corrupted files.
4. **Data Extraction**: For each valid file, extract the `Timestamp` and the string value of the key named `target_version`. If a file does not contain the `target_version` key, ignore it.
5. **Aggregation**: For each server (determined by the name of the immediate subdirectory containing the backup file), find the `target_version` associated with the *highest* valid `Timestamp`.
6. **Atomic Write**: Write the final aggregated results to `/home/user/config_summary.json` as a JSON object. To prevent partial writes in our concurrent environment, you *must* use an atomic write strategy (e.g., write to a temporary file in the same directory and use `os.replace` to overwrite `/home/user/config_summary.json`).

The final `/home/user/config_summary.json` must have the following format:
```json
{
  "server_name_1": {
    "latest_timestamp": 1620000000,
    "target_version": "v1.2.3"
  },
  "server_name_2": {
    "latest_timestamp": 1620005000,
    "target_version": "v2.0.1"
  }
}
```

Write and execute your Python script to generate the correct `/home/user/config_summary.json` file.