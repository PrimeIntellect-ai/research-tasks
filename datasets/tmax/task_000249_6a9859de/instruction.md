You are tasked with building a differential backup tool for a configuration manager that tracks changes in a poorly maintained directory structure.

The configuration directory is located at `/home/user/app_config`. Over time, users have created complex symbolic links inside this directory, some of which form infinite loops (e.g., a symlink pointing to its parent directory). 

Your objective is to create a backup of recently changed files while safely handling these symlink loops, merging the data, and storing it in chunked format using atomic operations.

Please perform the following steps:
1. Find all regular files within `/home/user/app_config` (following symlinks to files, but avoiding infinite directory loops) that have been modified in the last 24 hours. Ignore directories and broken symlinks.
2. Concatenate the contents of these recently modified files. The files must be concatenated in alphabetical order based on their base filenames (e.g., `a.conf` before `b.conf`).
3. Pipe the concatenated contents into the `split` command to divide the data into chunks of exactly 100 bytes each. Use the default naming scheme (`xaa`, `xab`, etc.).
4. To ensure atomic writes, you must first write these chunks to a temporary staging directory at `/home/user/staging_backup`.
5. Once all chunks are safely written to the staging directory, move all the chunk files atomically into the final backup directory at `/home/user/backup_chunks`.

Ensure that:
- You do not back up files older than 24 hours.
- You properly handle or bypass the infinite symlink loop without your script hanging or crashing.
- The final chunks reside directly in `/home/user/backup_chunks/` (e.g., `/home/user/backup_chunks/xaa`).

Write the necessary commands or scripts to accomplish this. You can use any combination of shell commands or scripting languages available on a standard Linux system.