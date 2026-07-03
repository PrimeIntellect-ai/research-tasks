You are managing binary repositories as an artifact manager. Your system receives proprietary artifact bundles and extracts them using a legacy tool. 

We have a stripped, closed-source extraction binary located at `/app/extractor`. This tool extracts custom `ARTF` archives, but it has a critical flaw: it blindly trusts the archive metadata. It will happily write files to absolute paths, follow `../` directory traversals, or create symlinks that result in infinite loops during backup scans.

Your task is to write a Python script `/home/user/filter_archive.py` that acts as a pre-extraction security filter. The script must take exactly one argument (the path to an `ARTF` archive), parse its metadata, and determine if it is safe to extract.

The script must exit with status `0` if the archive is completely safe, and status `1` if it is malicious or malformed.

**Archive Format Specification:**
*   **Magic Header:** First 4 bytes must be `ARTF`.
*   **Entries:** Followed by zero or more entries, sequentially packed:
    *   `path_length`: 2 bytes, unsigned little-endian integer.
    *   `path`: UTF-8 string of `path_length` bytes (the file path to extract to).
    *   `entry_type`: 1 byte, unsigned integer (`0` for standard file, `1` for symlink).
    *   `data_length`: 4 bytes, unsigned little-endian integer.
    *   `data`: Raw bytes of `data_length`. If `entry_type` is `1` (symlink), this data contains the UTF-8 target path of the symlink.

**Safety Rules (Reject with exit code 1 if any are violated):**
1. Any `path` or symlink target contains `../` or starts with `/` (absolute path).
2. Any symlink points to a directory loop (e.g., linking to its own parent or a recursive structure). For simplicity, reject any archive where a symlink target contains the name of the symlink itself or points to `.` as a directory component.
3. The file is truncated or misses the `ARTF` header.

Write the script at `/home/user/filter_archive.py`. You do not need to invoke `/app/extractor` yourself; an automated pipeline will run your script against a corpus of safe and malicious archives.