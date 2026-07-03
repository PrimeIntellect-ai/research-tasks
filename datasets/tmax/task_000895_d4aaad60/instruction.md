I am a technical writer managing a large documentation project, and I need an automated way to update outdated terminology across my files and create a differential backup.

I have a directory of Markdown files located at `/home/user/docs/`. 
I also have a configuration file at `/home/user/doc_config.ini` that defines a set of outdated terms and their replacements, as well as backup settings. 
Additionally, my previous full backup state is recorded in `/home/user/backups/snapshot.json`, which maps file paths (relative to `/home/user/docs/`) to their MD5 checksums at the time of the last backup.

Please write and execute a Python script (`/home/user/update_and_backup.py`) that performs the following:

1. **Configuration Interpretation**: Read `/home/user/doc_config.ini` to get the terminology mapping and the target backup directory.
2. **Large-scale text editing with Atomic Writes**: Iterate through all `.md` files in `/home/user/docs/`. Replace all occurrences of the outdated terms (keys in the config) with their replacements (values in the config). The terminology replacement must be case-sensitive. 
   *CRITICAL:* You must use atomic writes when modifying these files (e.g., write to a temporary file in the same directory, then overwrite the original file via a rename operation) to prevent corruption in case of a crash.
3. **Differential Backup**: After the updates are complete, compare the *new* MD5 checksums of all `.md` files against the ones in `/home/user/backups/snapshot.json`. 
   - If a file is new (not in the snapshot) or its checksum has changed after the updates, include it in a new compressed archive.
   - Create a tarball named `/home/user/backups/diff_backup.tar.gz` containing *only* these changed or new files. The files inside the tarball should retain their relative paths (e.g., `file1.md`, `subdir/file2.md`).
4. **Logging**: Create a log file at `/home/user/backups/backup_summary.txt` containing a sorted, newline-separated list of the relative paths of the files included in the differential backup.

Ensure your script handles everything end-to-end. Run it to produce the final updated documents, the tarball, and the log file.