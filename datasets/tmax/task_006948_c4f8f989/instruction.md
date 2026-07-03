You are an AI assistant helping a lead data researcher clean up and organize a newly acquired dataset before it is ingested into the main research cluster. 

The researcher suspects that one of the recently uploaded dataset archives might be malicious and contain a "Zip Slip" vulnerability—an archive crafted with file paths that attempt to traverse outside the intended extraction directory (e.g., using `../` or absolute paths).

You have two main objectives:

**1. Identify the Culprit**
There is a multi-line text log file located at `/home/user/logs/upload_events.log`. Each upload event spans multiple lines in the following exact format:
```
--- EVENT START ---
Timestamp: [YYYY-MM-DD HH:MM:SS]
User ID: [Username]
Uploaded File: [Filename]
Status: [SUCCESS/FAILED]
--- EVENT END ---
```
Parse this log file to find the `User ID` of the person who uploaded `data.zip` with a `Status` of `SUCCESS`. Write ONLY the username string to `/home/user/culprit.txt`.

**2. Safely Extract and Audit the Archive**
The untrusted dataset archive is located at `/home/user/incoming/data.zip`.
Write and execute a Python script to securely process this archive. Your script must:
* Inspect every file path in the archive.
* Determine if the path is safe or unsafe. A path is unsafe if, when extracted to a target directory, it would resolve to a location *outside* of that target directory (e.g., `../outside.txt`, `../../../etc/passwd`), or if it is an absolute path (e.g., `/var/tmp/bad.sh`).
* Extract ONLY the safe files into the directory `/home/user/clean_data/` (create this directory if it doesn't exist), maintaining their safe directory structure.
* Log the exact original archive paths of all unsafe/malicious files to `/home/user/zip_slip_detected.txt`, with one path per line. Do not extract these files.

Ensure your script handles path resolution robustly, as attackers might use complex traversals like `safe_dir/../../malicious.sh`.

Complete these tasks using the Linux terminal. Use Python for the archive processing.