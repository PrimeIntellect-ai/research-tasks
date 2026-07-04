You are a storage administrator responsible for managing an automated disk space quota system. Departments drop archive files into an incoming directory, and your system must extract them, parse their metadata to calculate quota usage, and ensure system security.

Recently, there was a security incident involving "Zip Slip" vulnerabilities—archives containing paths that traverse outside the target directory (e.g., paths starting with `/` or containing `../`).

Your task is to build a robust Bash-based ingestion service and process a batch of test archives.

**Requirements:**

1. **Environment Setup:**
   - Create directories: `/home/user/incoming`, `/home/user/extracted`, and `/home/user/scripts`.
   - Install any necessary packages (e.g., `inotify-tools`, `jq`, `unzip`).

2. **The Watcher Script (`/home/user/scripts/watcher.sh`):**
   - Write a Bash script that uses `inotifywait` to continuously monitor `/home/user/incoming/` for newly created or moved-in files.
   - When a `.zip` or `.tar.gz` file arrives, the script must process it automatically.

3. **Security (Zip Slip Detection):**
   - Before extracting, the script must inspect the archive's contents.
   - If ANY file inside the archive contains `../` in its path or starts with `/`, the archive must **not** be extracted.
   - Instead, append the base name of the malicious archive to `/home/user/security_alerts.log` (one filename per line) and delete the archive from the incoming directory.

4. **Extraction and Encoding Conversion:**
   - If the archive is safe, extract it into a subdirectory under `/home/user/extracted/` named after the archive (e.g., `archive.zip` extracts to `/home/user/extracted/archive/`).
   - Each valid archive contains a `metadata.csv` file (columns: `filename,owner,size_bytes`).
   - These CSV files might be encoded in UTF-16LE, ISO-8859-1, or other encodings. Your script must detect the encoding and convert `metadata.csv` to standard UTF-8.

5. **Quota Parsing (Structured Data):**
   - After converting to UTF-8, parse the CSV file (ignoring the header).
   - Aggregate the total `size_bytes` per `owner` across *all* safely extracted archives.
   - Maintain the global totals in a JSON file at `/home/user/storage_report.json` with the format:
     ```json
     {
       "alice": 1500,
       "bob": 250
     }
     ```
   - *Hint: The script can read the current JSON, update the counts, and write it back, or just recalculate it entirely whenever a new CSV is processed.*

6. **Execution:**
   - I have provided test archives in `/home/user/test_data/`.
   - Run your watcher script in the background.
   - Copy all files from `/home/user/test_data/` into `/home/user/incoming/`.
   - Wait a few seconds for the processing to finish, then terminate your watcher script.

Ensure your `storage_report.json` and `security_alerts.log` are strictly formatted and correct based on the test data.