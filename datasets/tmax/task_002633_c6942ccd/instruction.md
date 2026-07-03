You are acting as a storage administrator who is building a secure data ingestion pipeline for video surveillance archives. To optimize disk space, you need to extract frames from video files, manifest them, and build a secure extraction script to handle a custom archive format designed for this system.

Your task has two parts:

**Part 1: Video Frame Extraction & Manifest**
There is a surveillance video located at `/app/surveillance.mp4`.
1. Use `ffmpeg` to extract frames from this video at a rate of 1 frame per second. Save them in `/home/user/frames/` with the naming convention `frame_001.jpg`, `frame_002.jpg`, etc.
2. Generate a JSON manifest at `/home/user/manifest.json`. It should be a dictionary mapping the base filename (e.g., `"frame_001.jpg"`) to its lowercase SHA256 checksum.

**Part 2: Secure Archive Parser**
To receive archives from remote cameras, you must write a strict, safe parser in Python to prevent malicious path-traversal (Zip Slip) attacks.
Write a script at `/home/user/parse_archive.py`. This script must read a custom binary format called `VARC` from `stdin` and print the actions it *would* take to `stdout`. It should not actually write any files to disk.

**VARC Format Specification:**
- **Magic Header:** 4 bytes, ASCII string `VARC`.
- **Entry Count:** 2 bytes, unsigned integer (big-endian), indicating the number of files in the archive.
- **Entries** (repeated Entry Count times):
  - **Path Length:** 2 bytes, unsigned integer (big-endian).
  - **Path:** UTF-8 string of `Path Length` bytes.
  - **Data Length:** 4 bytes, unsigned integer (big-endian).
  - **Data:** Raw bytes of `Data Length`.

**Security & Output Rules:**
Iterate through the entries. For each entry:
1. **Path Traversal Check:** If the `Path` starts with `/` or contains `../` anywhere, it is malicious. You must print EXACTLY: `[REJECT] <path>` (e.g., `[REJECT] ../../../etc/shadow`). Skip its data and move to the next entry.
2. **Valid File:** If the path is safe, print EXACTLY: `[ACCEPT] <path> <data_length> <sha256_hex_of_data>`.
3. **Truncation:** If `stdin` ends unexpectedly before an entry is fully read (or if the magic header is wrong), immediately print `[ERROR] invalid or truncated archive` to `stdout`, and exit the script with exit code `1`.
4. **Success:** If the archive is successfully parsed to completion, exit with code `0`.

Ensure your script is robust and processes binary streams precisely. We will test your script using an automated fuzzing suite that compares your script's output bit-for-bit against a highly secure reference oracle.