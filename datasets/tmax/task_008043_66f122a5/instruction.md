You are a backup administrator tasked with recovering and consolidating differential backup data from a legacy storage system.

An old backup routine dumped nested archives across a deeply structured directory. We need to extract this data, identify the newly modified files (simulating an incremental backup), and package them into a clean, consolidated archive.

System State:
- You have a directory at `/home/user/legacy_backups/` containing various subdirectories.
- Inside these subdirectories are `.zip` files. 
- Inside each `.zip` file is a `.tar` file.
- Inside the `.tar` files are the actual data files.
- There is a reference file at `/home/user/last_backup.ref` which represents the timestamp of our last successful full backup.

Your task:
1. Traverse the `/home/user/legacy_backups/` directory and extract all nested archives (extract the `.zip` files, then extract the `.tar` files found inside them) into a flat or structured staging directory at `/home/user/restored/`. Ensure that the original file modification times (mtimes) are preserved during both extraction steps.
2. Identify all data files in `/home/user/restored/` (and its subdirectories) that are strictly *newer* than the reference file `/home/user/last_backup.ref`.
3. Create a new gzipped tar archive at `/home/user/incremental_update.tar.gz` containing *only* these newer files.
4. When creating the final archive, execute the `tar` command from within the `/home/user/restored/` directory so that the paths inside the archive are relative (e.g., `file2.txt` or `./file2.txt`, not `/home/user/restored/file2.txt`).

Please write and execute the Bash commands or scripts required to complete this task. The task will be evaluated by verifying the contents of `/home/user/incremental_update.tar.gz`.