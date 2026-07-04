You are a backup administrator responsible for managing a legacy system that uses a proprietary "Custom Backup Archive" (`.cba`) format. Recently, a vulnerability (similar to Zip Slip) was discovered in the old extraction tool, allowing malicious archives to overwrite system files by using directory traversal sequences (like `../`) in the filenames. Furthermore, the archives often contain a mix of junk files, and you only need to recover specific database Write-Ahead Logs (WAL) and ELF executables.

Your task is to write a secure Python extraction tool at `/home/user/extract_backup.py` and use it to process a backup file located at `/home/user/backups/daily.cba`.

### The `.cba` Format Specification
The `.cba` file is a binary file with the following structure:
1.  **Magic Bytes:** The first 2 bytes are always `CB` (ASCII).
2.  **File Count:** The next 4 bytes represent the number of files in the archive (unsigned 32-bit integer, little-endian).
3.  **File Entries:** For each file, the following sequence occurs:
    *   **Filename Length ($N$):** 2 bytes (unsigned 16-bit integer, little-endian).
    *   **Filename:** $N$ bytes (UTF-8 encoded string). May contain relative paths.
    *   **Compressed Size ($S$):** 4 bytes (unsigned 32-bit integer, little-endian).
    *   **File Data:** $S$ bytes of `zlib` compressed data.

### Tool Requirements (`/home/user/extract_backup.py`)
Your script must take two arguments: the input archive path and the output directory path.
```bash
python3 /home/user/extract_backup.py /home/user/backups/daily.cba /home/user/restored
```

**1. Path Traversal Prevention (Zip Slip Mitigation)**
As you iterate through the archive, resolve the absolute path for each file relative to the output directory. If the resolved path falls *outside* the designated output directory, you must **NOT** extract the file. Instead, append the exact malicious filename string (as it appeared in the archive) to a log file at `/home/user/zip_slip.log`, with each skipped filename on a new line.

**2. Domain-Specific Filtering**
For files that pass the security check, decompress their data using `zlib`. You must only extract files that match one of the following magic byte signatures at the start of their **decompressed** data:
*   **WAL Files:** First 4 bytes must be exactly `WAL\x00`.
*   **ELF Binaries:** First 4 bytes must be exactly `\x7fELF`.
Files failing this check should be silently ignored (do not write them to disk and do not log them).

**3. Atomic Writes & Temp File Management**
To prevent partial files from being created if the system crashes during decompression or disk writing, you must use atomic writes. Write the decompressed data to a temporary file in the output directory (e.g., using `.tmp` extension), and only rename it to the final target filename once the write is completely successful and the file is closed. Ensure any required subdirectories inside the output directory are created before writing.

### Execution
1. Create the `/home/user/restored` directory.
2. Write the extraction script.
3. Run your script to extract `/home/user/backups/daily.cba` into `/home/user/restored`.