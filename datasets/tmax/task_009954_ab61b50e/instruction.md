You are tasked with recovering configuration change data from a legacy configuration manager's backup system. The backup system stores its write-ahead logs (WAL) in nested archives.

You have been provided with an archive file at `/home/user/config_backups.zip`.

Your objective is to:
1. Extract the nested archives. Inside the zip, you will find `logs_2023.tar.gz` and `logs_2024.tar.gz`. You only care about the 2024 logs.
2. Inside `logs_2024.tar.gz`, there are multiple binary WAL files with a `.wal` extension.
3. Parse the `.wal` files to extract specific configuration changes.
4. Output the extracted changes to a JSON file at `/home/user/network_changes.json`.

**Custom WAL Binary Format Specification:**
*   **Header (5 bytes):**
    *   Magic number: 4 bytes representing the ASCII string "CWAL"
    *   Version: 1 byte (unsigned integer). Expected to be `1`.
*   **Records (Repeated until EOF):**
    *   Timestamp: 4 bytes (Little-endian unsigned integer, Unix epoch time)
    *   Action type: 1 byte (unsigned integer). `1` = ADD, `2` = MOD (Modify), `3` = DEL (Delete)
    *   Key Length: 2 bytes (Little-endian unsigned integer)
    *   Key: UTF-8 string of 'Key Length' bytes
    *   Value Length: 2 bytes (Little-endian unsigned integer)
    *   Value: UTF-8 string of 'Value Length' bytes

**Filtering and Output Requirements:**
You must parse all `.wal` files from the 2024 archive and find every record that matches BOTH of these criteria:
*   The Action type is `2` (MOD).
*   The Key contains the substring `network` (case-sensitive).

Convert the matched records into a JSON array of objects. Write this JSON array to `/home/user/network_changes.json`.
Each object in the JSON array must have the following keys:
*   `timestamp` (integer)
*   `key` (string)
*   `value` (string)

The JSON array should be sorted by `timestamp` in ascending order. If two records have the same timestamp, sort them alphabetically by `key`.

You may use any language available (like Python, Bash, etc.) to write a script to achieve this.