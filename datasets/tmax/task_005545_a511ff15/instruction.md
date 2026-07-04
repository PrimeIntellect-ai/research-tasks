You are managing a custom configuration tracking system. The system takes configuration backups and stores them in a proprietary custom binary format with the extension `.snap`. 

You need to write a Python script at `/home/user/parse_snaps.py` that processes a directory of these snapshots located at `/home/user/snapshots/`. Your script must verify the integrity of each snapshot, extract its contents, parse the configuration changelog, and generate a JSON report.

**The `.snap` File Format:**
Each `.snap` file is a binary file with the following structure:
1. **Magic Bytes (4 bytes):** The ASCII string `SNAP` (i.e., `0x53 0x4E 0x41 0x50`).
2. **Version (2 bytes):** An unsigned 16-bit integer, little-endian.
3. **Checksum (16 bytes):** The MD5 hash of the *entire remainder* of the file (the payload).
4. **Payload (Variable length):** A standard `tar.gz` archive.

**Processing Requirements:**
1. Read each `.snap` file in `/home/user/snapshots/`.
2. Extract the binary header. If the magic bytes are not `SNAP`, skip the file.
3. Calculate the MD5 hash of the Payload. If it does not strictly match the 16-byte Checksum in the header, the file is corrupted. You must **skip** corrupted files.
4. For valid files, extract the `tar.gz` payload in memory or to a temporary directory.
5. Inside the archive, there is a file named `changelog.txt`. It contains a multi-line log record formatted exactly like this:
   ```
   Commit: <commit_hash>
   Author: <author_name>
   Changes:
    - <change item 1>
    - <change item 2>
    - <change item 3>
   ```
   *Note: The number of changes varies. The record ends at the end of the file.*
6. Parse this log to extract the `commit`, `author`, and the list of `changes` (stripping the leading ` - ` and any trailing whitespace).
7. Output the parsed data for all **valid** snapshots as a single JSON array to `/home/user/report.json`.

**Output Format (`/home/user/report.json`):**
The JSON array must be sorted alphabetically by the `.snap` filename.
```json
[
  {
    "filename": "backup_01.snap",
    "version": 1,
    "commit": "a1b2c3d",
    "author": "devops_alice",
    "changes": [
      "Updated nginx.conf workers",
      "Added rate limiting"
    ]
  }
]
```

Write the Python script, execute it, and ensure `/home/user/report.json` is created with the correct format.