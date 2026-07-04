You are assisting a backup administrator in archiving and verifying historical server data. 

There is a directory located at `/home/user/backups/server_alpha` containing a mix of plain files and compressed archives (`.zip` and `.tar.gz`). These directories and archives contain various `.log` files and `.bin` files.

Your task is to write and execute a Python script that recursively traverses this directory and processes the files as follows:

1. **Log Files (`.log`)**:
   - Find every `.log` file, whether it is a plain file on the disk or packed inside a `.zip` or `.tar.gz` archive.
   - Extract exactly the last 3 lines of each `.log` file. (If a file has fewer than 3 lines, extract all of them).
   - Write the results to `/home/user/backup_logs_tail.txt`.
   - The format for each log file in the output must be:
     `=== {filepath} ===`
     `[line 1]`
     `[line 2]`
     `[line 3]`
   - For files inside archives, `{filepath}` should be formatted as `{path_to_archive}::{internal_file_path}`. For plain files, it is just the relative path from `/home/user/backups/server_alpha/` (e.g., `db/sync.log` or `web/old_logs.tar.gz::access.log`).
   - The entries in `/home/user/backup_logs_tail.txt` must be sorted alphabetically by the `{filepath}` string.

2. **Binary Files (`.bin`)**:
   - Find every `.bin` file (plain or inside archives).
   - Compute the SHA-256 checksum of the binary data.
   - Write the results to `/home/user/backup_bin_manifest.txt`.
   - The format must be: `{sha256_hex}  {filepath}` (two spaces between hash and path).
   - The `{filepath}` rules are the same as above.
   - The entries in `/home/user/backup_bin_manifest.txt` must be sorted alphabetically by the `{filepath}` string.

Write the Python script, execute it, and ensure the two output files `/home/user/backup_logs_tail.txt` and `/home/user/backup_bin_manifest.txt` are created with the exact specified formats. Treat all `.log` files as UTF-8 encoded text files.