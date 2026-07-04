You are tasked with building a secure backup ingestion service in Python to handle archive files from remote systems.

First, inspect the image file located at `/app/backup_policy.png`. This image contains a printed policy ID. You must use optical character recognition (OCR) to read the text from this image (look for a string formatted like `POLICY_ID: <PREFIX_TEXT>`). You will use `<PREFIX_TEXT>` as the prefix for renaming files.

Write a Python HTTP server (you can use Flask, FastAPI, or the standard library) that listens on `127.0.0.1:9000`. 
The server must have a single endpoint `POST /upload` that accepts `multipart/form-data` containing a ZIP file under the field name `archive`.

When a ZIP file is uploaded, the server must process it as follows:
1. **Safe Extraction**: Extract the contents of the ZIP file into the directory `/home/user/backup_vault/`. However, some incoming archives might be malicious. You must protect against "Zip Slip" attacks. Any file entry in the ZIP that attempts to extract outside of `/home/user/backup_vault/` (e.g., using `../` traversals) MUST be skipped or rejected.
2. **Bulk Renaming**: Every successfully extracted file must be renamed such that its base filename is prefixed with the `<PREFIX_TEXT>` extracted from the image. For example, if the prefix is `ABC_` and the file is `data/logs.txt`, it should become `data/ABC_logs.txt`.
3. **Deduplication via Hard Links**: To save space, your service must identify duplicate files within the extracted batch. If multiple files have the exact same contents, only the first processed file should exist as a regular file. All subsequent duplicates must be replaced with hard links pointing to the first file.

Requirements:
- Ensure the directory `/home/user/backup_vault/` is created if it does not exist.
- Keep the server running in the foreground or background so it can receive requests.
- Log successfully processed files to standard output.