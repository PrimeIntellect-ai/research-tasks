You are an artifact manager AI responsible for curating binary repositories. Your task is to implement and execute an incremental backup system for our primary artifact repository.

You have a configuration file located at `/home/user/repo_config.ini` and a previous backup manifest located at `/home/user/backups/manifest_v1.json`. The repository itself is located at `/home/user/repo/`.

Your objective is to write and execute a Python script that performs the following steps:

1. **Configuration Parsing & Navigation:** Read `/home/user/repo_config.ini`. It contains a `[Backup]` section with `include_dirs` (comma-separated list of directories to back up) and `exclude_patterns` (comma-separated list of glob patterns to ignore).
2. **Manifest Generation:** Traverse the included directories. For every file that does *not* match any of the exclude patterns, compute its SHA-256 checksum. Generate a new manifest file at `/home/user/backups/manifest_v2.json`. The manifest must be a JSON object mapping relative file paths (relative to `/home/user/repo/`) to their hex-encoded SHA-256 hashes.
3. **Differential Analysis:** Compare your new manifest against `/home/user/backups/manifest_v1.json`. Identify files that are either new or have been modified (i.e., their hash has changed).
4. **Archive Creation:** Create a compressed archive at `/home/user/backups/incremental_v2.tar.gz` containing *only* the new and modified files. The files inside the tarball should maintain their structure relative to `/home/user/repo/` (e.g., `bin/app_v2`, not `/home/user/repo/bin/app_v2`).
5. **Summary Log:** Create a text file at `/home/user/backups/backup_summary.txt`. For each file added to the archive, write a line in the format:
   `NEW: <relative/path>` (if the file was not in v1)
   `MODIFIED: <relative/path>` (if the file was in v1 but the hash changed)
   Sort the lines alphabetically by file path.

Ensure all output paths strictly match the requirements. Do not include files from directories not specified in `include_dirs`, and correctly apply the `exclude_patterns`.