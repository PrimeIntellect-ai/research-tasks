You are helping a technical writer securely process incoming documentation updates from third-party contributors. These updates are delivered as compressed archives, but some contributors have poorly configured archiving tools that include absolute paths or parent directory traversals (`../`), which could overwrite files outside the intended documentation folder (a Zip Slip vulnerability).

Your task is to write and execute a Python script at `/home/user/extract_docs.py` that safely extracts an incoming tarball while strictly preventing path traversal attacks and ensuring atomic file updates.

Here are the requirements:
1. The incoming archive is located at `/home/user/incoming/update.tar.gz`.
2. The target extraction directory is `/home/user/docs/`.
3. Your Python script must iterate through the compressed archive. For each file member:
   - Determine its absolute target path if extracted into `/home/user/docs/`.
   - If the resolved absolute target path does not strictly start with `/home/user/docs/`, you must reject the file.
   - If it is a valid file, extract its contents to the target location securely using an atomic write: write the extracted data to a temporary file in the same directory as the target (e.g., append `.tmp` to the filename), and then atomically rename it to the final filename. (You must create any required parent directories for valid nested files).
4. Do not extract directory members directly, only file members.
5. Create a log file at `/home/user/extraction_log.txt`. For every file member in the archive, write exactly one line in the following format:
   - If successfully extracted: `EXTRACTED: <target_absolute_path>`
   - If rejected due to path traversal/absolute path: `REJECTED: <member_name_in_archive>`
   Sort the log lines alphabetically before writing them to the log file.

Write the script, execute it to process `/home/user/incoming/update.tar.gz`, and ensure the log file is generated.