You are a technical writer tasked with organizing and validating automated documentation artifacts. A background process continuously captures screencasts and packages them into documentation archives. However, a race condition in the log rotation script sometimes produces corrupted, incomplete, or tampered archives. 

Your objective is to create a robust validator that filters out invalid documentation archives while accepting valid ones. 

First, extract a reference frame from the documentation screencast located at `/app/screencast.mp4` at exactly the 00:00:10 mark. Save this extracted image as `/home/user/reference_frame.jpg`.

Next, write a script (in bash, Python, or your preferred language) at `/home/user/validate_doc_archive.sh` that takes a single argument: the path to a documentation archive (`.tar.gz`). 

The script must exit with status `0` (accept) for valid archives and a non-zero status (e.g., `1`) (reject) for invalid archives.

Validation Rules:
1. **Concurrency Control**: The script must attempt to acquire an exclusive lock on `<archive_path>.lock` before processing the archive. If it cannot acquire the lock within 2 seconds, it must assume the file is currently being written to and reject it.
2. **Structure**: The archive must be a valid `.tar.gz` file. When extracted, it should contain at least `manifest.json`, `metadata.csv`, and `frame.jpg`.
3. **Manifest Integrity**: `manifest.json` must be valid JSON containing a dictionary of filenames to SHA-256 checksums (e.g., `{"frame.jpg": "abc...", "metadata.csv": "def..."}`).
4. **Checksum Verification**: Every file listed in the manifest must exist in the extracted archive, and its SHA-256 checksum must perfectly match the value in the manifest.
5. **Security / Path Traversal**: Reject the archive if any filename in the manifest contains directory traversal sequences (`..`) or absolute paths (starting with `/`).
6. **Reference Matching**: Read `metadata.csv`. If the CSV (which has a header `type,value`) contains a row where `type` is `reference` and `value` is `true`, the `frame.jpg` in the archive must have the exact same SHA-256 checksum as your extracted `/home/user/reference_frame.jpg`.

Your solution will be tested against two sets of archives:
- A "clean" corpus of perfectly valid archives.
- An "evil" corpus containing archives that violate one or more of the rules above (e.g., corrupted JSON, mismatched checksums, path traversal attempts, incorrect reference frames, or simulated locked files).

Your script must accept 100% of the clean archives and reject 100% of the evil archives. Ensure `/home/user/validate_doc_archive.sh` is executable and uses the correct shebang.