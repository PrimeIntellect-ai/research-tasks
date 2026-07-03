You are tasked with restoring a project's files from a series of backups. I have a `/home/user/backups` directory containing several archive files and a log file named `/home/user/backups/backup.log`. 

The `backup.log` file contains multi-line records of the backups, but they are out of order. Each record looks something like this:
```
=== Backup Record ===
ID: [Integer]
Date: [YYYY-MM-DD]
File: [filename]
Type: [Full or Incremental]
=====================
```

Your objective is to safely restore the project state to `/home/user/project_restore` using Python:
1. Parse `backup.log` to determine the correct chronological order of the backups based on the `Date` field.
2. Extract the files from the nested/incremental backups into `/home/user/project_restore` in that exact chronological order (the "Full" backup is first, followed by "Incremental" backups). 
3. **Security Requirement:** One or more of the archives may be corrupted or malicious, containing paths that attempt to escape the target directory (e.g., using `../` or absolute paths). You must write a Python script to perform the extraction safely. Any file inside an archive that would extract outside of `/home/user/project_restore` must be skipped.
4. If a file is skipped due to this security check, append the original malicious path from the archive (e.g., `../some_file.txt`) to a log file at `/home/user/skipped.log` (one path per line).
5. Once all archives are successfully and safely extracted, generate a manifest of the final project state. Create a JSON file at `/home/user/manifest.json` where the keys are the relative file paths (e.g., `src/app.py`) and the values are the SHA-256 checksums of the restored files. Do not include directories in the JSON manifest, only files.

Ensure your Python script handles the extraction securely and generates the precise outputs requested.