You are a storage administrator managing a massive file ingestion pipeline. Users upload archive files, which are later extracted to internal storage. Recently, you discovered that some malicious users are attempting "Zip Slip" attacks—crafting archives with file paths designed to overwrite system directories (e.g., using `../` or absolute paths). 

We have a custom, vendored Python package named `py-archive-validator` that is supposed to prevent this, but it appears to have a security flaw. 

Your tasks:

1. **Fix the Vendored Package:**
   Inspect the source code of the vendored package located at `/app/py-archive-validator-1.0.0/`. Specifically, look at `validator/core.py`. The path validation logic contains a deliberate bug/oversight that allows certain traversal attacks to bypass the filter. Fix the logic in this package so that it correctly identifies any path that would escape a target extraction directory. (Do not rely on the OS to block it; the function must return `False` for unsafe paths).

2. **Develop the Classifier:**
   Write a Python CLI script at `/home/user/scan.py`. This script must:
   - Accept a single command-line argument: the path to a directory containing `.zip` files.
   - Import and use the fixed `py-archive-validator` package to evaluate every `.zip` file in the directory.
   - Output a file named `/home/user/results.json` containing a single dictionary mapping the filename (e.g., `archive1.zip`) to its classification string.
   - The classification string must be:
     - `"invalid"` if the file is not a valid zip archive (archive integrity verification).
     - `"evil"` if the zip archive contains *any* unsafe file paths according to the validator.
     - `"clean"` if the zip archive is valid and all file paths are safe.

3. **Identify the Malicious User:**
   We have a multi-line log file of recent uploads at `/app/upload_service.log`. The log format spans multiple lines per upload:
   ```
   [START UPLOAD]
   Timestamp: 2023-10-01T12:00:00Z
   User: <username>
   Archive: <filename.zip>
   [END UPLOAD]
   ```
   Using your fixed classifier, scan the directory `/app/recent_uploads/`. Then, parse the `upload_service.log` file, cross-reference the filenames with your classification results, and determine which `User` uploaded the highest number of `"evil"` archives. 
   Write the username of this top offender to `/home/user/banned.txt`.

Ensure your script handles corrupt binary files gracefully and produces the exact JSON format requested.