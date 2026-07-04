You are an AI assistant helping a storage administrator free up disk space by cleaning up old, proprietary archive files.

The administrator has a directory of custom write-ahead log backups located at `/home/user/backups`. These backups can be extremely large, so loading them entirely into memory is not feasible. You must use Go to build a cleanup tool that uses streaming I/O to read only the headers of these files.

Each backup file has a `.wal` extension and uses the following custom binary structure:
1. **Magic Bytes (4 bytes):** The ASCII string `WALB`.
2. **Creation Timestamp (4 bytes):** An unsigned 32-bit integer in Big-Endian format representing a UNIX epoch timestamp.
3. **Payload Length (4 bytes):** An unsigned 32-bit integer in Big-Endian format.
4. **Embedded ELF Binary:** Starting at byte offset 12, there is an embedded ELF file. 

Your cleanup tool must:
1. Read a configuration file located at `/home/user/config.json`. This file contains:
   `{"cutoff_time": 1600000000, "backup_dir": "/home/user/backups", "report_file": "/home/user/cleanup_report.txt"}`
2. Iterate through all `.wal` files in the `backup_dir`.
3. Read the binary header using Go's `io.Reader` or similar streaming constructs (read *only* what is necessary).
4. Verify the `WALB` magic bytes.
5. If the Creation Timestamp is **strictly less than** the `cutoff_time`, the backup is considered expired.
6. For expired backups, extract the `e_machine` field from the embedded ELF header. In an ELF header, the `e_machine` field is a 16-bit unsigned integer (Little-Endian) located at offset 18 from the start of the ELF file (which means it's at offset 30 from the start of the `.wal` file).
7. Append a record of the expired backup to the `report_file` (specified in the config) exactly in this format:
   `<filename>: <timestamp>, arch: 0x<e_machine_hex_lowercase>`
   Example: `backup_1.wal: 1500000000, arch: 0x3e`
8. Delete the expired `.wal` file to free up disk space. Do not delete files that are equal to or newer than the `cutoff_time`.

Write and execute your Go program at `/home/user/cleanup.go`. Ensure your program successfully processes the backups and leaves the system in the correct state.