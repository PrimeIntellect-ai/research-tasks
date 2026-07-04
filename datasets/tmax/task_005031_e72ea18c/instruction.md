You are a backup administrator tasked with recovering and sanitizing a legacy data archive. You have been given a scanned memo containing the current backup policy, a legacy multi-part archive, and you need to process the data according to the rules.

Your tasks are:

1. **Read the Backup Policy:** 
   Analyze the scanned memo located at `/app/policy.png` (you may use `tesseract` or similar tools). The memo contains three critical pieces of information:
   - The specific legacy character encoding used in the old files.
   - A specific prefix that must be added to all backed-up files.
   - A specific text signature that indicates a file is corrupted/malicious and must NOT be backed up.

2. **Develop a Backup Filter:**
   Write a Python script at `/home/user/backup_filter.py`. The script must accept a single argument (the absolute path to a file):
   `python3 /home/user/backup_filter.py <path_to_file>`
   - The script must exit with status code `0` if the file is clean and should be backed up.
   - The script must exit with status code `1` if the file contains the malicious signature identified in the memo.
   *(Note: An automated verification system will test this script against a hidden dataset of thousands of clean and malicious files to ensure it correctly implements the policy).*

3. **Extract and Process the Legacy Data:**
   - In `/app/legacy_data/`, there is a multi-part split zip archive (`archive.zip.001`, `archive.zip.002`, etc.). Reassemble and extract it. Inside, you will find nested tarballs. Extract all nested files.
   - For every extracted file, run your `backup_filter.py`. 
   - If the file is rejected by the filter, delete it.
   - If the file passes the filter:
     a) Convert its text encoding from the legacy encoding (specified in the memo) to `UTF-8`.
     b) Bulk rename the file: replace all spaces in the filename with underscores (`_`), and prepend the prefix specified in the memo.
     c) Save the final processed files into the directory `/home/user/processed_backup/`.

Ensure your `backup_filter.py` script is robust and your final `/home/user/processed_backup/` directory contains only the properly encoded, properly named, clean files.