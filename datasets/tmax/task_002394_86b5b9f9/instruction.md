You are helping a developer organize and secure a messy legacy project directory located at `/home/user/legacy_project`. The project contains unsorted binary assets and log files with sensitive information. You need to sanitize the text data, categorize the binary data by reading file headers, and set up an incremental backup system.

Please complete the following phases:

**Phase 1: Log Sanitation**
1. Search for all files ending in `.log` anywhere within `/home/user/legacy_project/`.
2. Using a tool like `sed`, `awk`, or Python, sanitize these log files *in place* by replacing all email addresses with the exact string `[REDACTED]`. (Assume standard email formatting: `string@string.tld`).

**Phase 2: Binary Asset Categorization**
1. In the `/home/user/legacy_project/assets/` directory, there are several files without extensions. 
2. Write a Python script at `/home/user/organize_binaries.py` that reads the first 4 bytes (magic numbers) of every file in the `assets/` directory.
3. The script should create the following directories and move the files into them based on their headers:
   - Move to `/home/user/legacy_project/organized/elf/` if the header is `\x7fELF`
   - Move to `/home/user/legacy_project/organized/png/` if the header is `\x89PNG`
   - Move to `/home/user/legacy_project/organized/unknown/` for all other files.

**Phase 3: Incremental Backups**
1. Create a directory `/home/user/backups/`.
2. Create a full `tar` backup of the entire `/home/user/legacy_project/` directory named `/home/user/backups/backup_full.tar`. You MUST use a tar snapshot file located at `/home/user/backups/project.snar` to track the state.
3. After the full backup is created, create a new text file at `/home/user/legacy_project/organized/update.txt` containing the text "Backup test".
4. Finally, create an incremental backup named `/home/user/backups/backup_inc.tar` using the same snapshot file `/home/user/backups/project.snar`.

Ensure all tasks are executed successfully. Do not delete the original files unless explicitly asked to move them.