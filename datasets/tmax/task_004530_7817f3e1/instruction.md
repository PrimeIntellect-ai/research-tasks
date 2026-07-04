You are an AI assistant helping a storage administrator clean up disk space by removing malicious or corrupted archive log files. The backup system produces multi-line log files for every archive operation, but a recent vulnerability allowed bad actors to inject forged log files containing malicious mount points and path traversal attacks.

Your task is to build a high-performance log filtering tool in Rust that identifies whether an archive log file is "Clean" (valid and safe) or "Evil" (malicious or corrupted).

Here are the specific requirements:

1. **Policy Extraction**:
   There is an image of a handwritten sticky note at `/app/policy_note.png`. Use `tesseract` to read this image. It contains the strict `ALLOWED_MOUNT_PREFIX` that all valid archives must reside within.

2. **Log File Format**:
   The log files you must parse contain multi-line records formatted exactly like this:
   ```
   [ARCHIVE_RECORD]
   ID=<numeric_id>
   MOUNT=<absolute_path>
   SIZE=<bytes>
   [END_RECORD]
   ```
   A log file may contain multiple such records.

3. **Classification Rules**:
   A log file is considered **Clean** if and only if ALL of the following are true for EVERY record in the file:
   - The file perfectly follows the multi-line format (every `[ARCHIVE_RECORD]` is eventually closed by an `[END_RECORD]`, with `ID`, `MOUNT`, and `SIZE` lines in between).
   - The `MOUNT` path strictly starts with the `ALLOWED_MOUNT_PREFIX` extracted from the image.
   - The `MOUNT` path contains absolutely no path traversal components (e.g., it must not contain `/../` or end in `/..`).

   If ANY record in the file violates these rules, or if the file contains garbage data outside the records, the entire file is considered **Evil**.

4. **Implementation details**:
   - Write your tool in Rust. Create your cargo project at `/home/user/archiver_cleanup`.
   - Your compiled binary must be located at `/home/user/archiver_cleanup/target/release/log_filter` (build it using `cargo build --release`).
   - The binary must accept exactly one command-line argument: the absolute path to a log file.
   - Your tool must utilize efficient I/O (e.g., `BufReader` streaming or `memmap2`) to handle potentially large files.
   - **Exit Codes**: The binary MUST exit with code `0` if the file is Clean (preserve), and exit with code `1` if the file is Evil (reject/delete).

5. **Verification**:
   An automated test will run your compiled binary against two hidden directories of log files (an "evil" corpus and a "clean" corpus). Your tool must achieve 100% accuracy, rejecting all evil files and preserving all clean files.