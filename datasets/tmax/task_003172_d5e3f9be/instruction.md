You are tasked with stepping in for a backup administrator to build a secure extraction utility for a proprietary backup format (`.sbk`). Recently, a security audit revealed that the previous extraction tool was vulnerable to "Zip Slip" attacks (where malicious archives overwrite files outside the target extraction directory) and lacked concurrency controls.

Your objective is to perform two main tasks:

**Part 1: Video Artifact Analysis**
The previous administrator left behind a corrupted environment, but secured the backup encryption salt in a video artifact located at `/app/evidence.mp4`.
1. Use `ffmpeg` (preinstalled) to extract the exact frame at `00:00:05.000` from `/app/evidence.mp4`. Save it as a PNG file.
2. Compute the SHA-256 hash of this PNG file. This hexadecimal hash string is your `SALT`.

**Part 2: Secure Extractor Implementation**
Write a Python script at `/home/user/safe_extract.py` that safely extracts `.sbk` archives. The script will be invoked as follows:
`python3 /home/user/safe_extract.py <path_to_sbk_file> <target_output_dir> <salt>`

**The `.sbk` (Secure Backup) Format Specification:**
1. **Magic Bytes:** The first 4 bytes of the file are exactly `SBK1` (ASCII).
2. **Manifest Length:** The next 4 bytes represent an unsigned 32-bit integer (little-endian) specifying the length `L` of the manifest in bytes.
3. **Manifest:** The next `L` bytes contain a UTF-8 encoded JSON string. The JSON is a list of dictionaries, where each dictionary represents a file to be extracted. Example:
   `[{"path": "config/settings.txt", "size": 1024, "checksum": "a1b2...", "offset": 0}, ...]`
   - `path`: The relative path where the file should be extracted.
   - `size`: The size of the file data in bytes.
   - `checksum`: The expected SHA-256 hex digest.
   - `offset`: The byte offset of the file's data *relative to the start of the data section*.
4. **Data Section:** The raw file data immediately follows the manifest.

**Extraction Requirements:**
1. **Directory Traversal / Zip Slip Protection:** You must strictly prevent any file from being extracted outside of `<target_output_dir>`. If a `path` attempts to traverse out (e.g., uses `../` escaping the root, or is an absolute path), you must completely skip extracting that file.
2. **Checksum Verification:** Before writing a file, you must verify its integrity. The checksum is computed as: `SHA256(file_data_bytes + salt.encode('utf-8'))`. If the computed hex digest does not match the manifest's `checksum`, skip the file.
3. **Recursive Directory Creation:** For valid files, ensure all parent directories exist before writing.
4. **Concurrency via File Locking:** Multiple extraction processes might run simultaneously targeting the same output directory. Before your script creates or writes to any extracted file, it must acquire an exclusive lock on a file named `.extraction_lock` located at the root of `<target_output_dir>`. Use `fcntl.flock`. Keep the lock acquired for the entire duration of the writing phase, and release it just before the script exits.
5. **Output:** The script must not print anything to standard output unless it encounters a fatal error (e.g., missing magic bytes), in which case it should print an error message and exit with a non-zero status. Invalid files (zip slip, bad checksum) should simply be skipped silently.

Ensure your script is robust. It will be rigorously tested against hundreds of generated `.sbk` files containing both valid data and adversarial payloads (e.g., zip slip attacks, malformed paths, and corrupted payloads) to ensure exact binary equivalence with a secure reference implementation.