You are tasked with helping a technical writing team stabilize their automated documentation backup and organization system. 

Our documentation environment currently consists of three running services:
1. **Nginx** serving the live documentation on port 8080 from `/app/docs_live`.
2. **DocGen Service** (a local process) constantly updating, modifying, and symlinking markdown and HTML files in `/app/docs_workdir` on port 5000.
3. **Redis** on port 6379, which DocGen uses to queue pending documentation rebuilds.

The technical writing team keeps creating circular symlinks in `/app/docs_workdir` that cause our current backup script to crash with infinite recursion. Additionally, because DocGen writes continuously, backups often read partially written files, leading to corrupted snapshots.

Your task is to write a robust Python backup tool at `/home/user/doc_backup.py` that implements safe differential backups, file locking, and manifest generation.

Requirements for `/home/user/doc_backup.py`:
1. **Command Line Interface:** The script must accept two arguments: an input directory and an output manifest path. Example: `python3 /home/user/doc_backup.py /app/docs_workdir /home/user/manifest.json`.
2. **Symlink Loop Prevention:** The script must traverse the input directory recursively. It must follow symlinks but strictly avoid infinite loops. If a symlink points to an already visited directory in the current traversal path, it should be skipped.
3. **Concurrent Access Handling:** Before reading any regular file to generate its backup checksum, you must acquire a shared lock (using `fcntl.flock` with `LOCK_SH`). If the lock cannot be acquired immediately (e.g., if DocGen is writing to it with an exclusive lock), skip the file and log a warning to standard error. Release the lock after reading.
4. **Manifest Generation:** Generate a JSON manifest file at the given output path. The JSON should be a dictionary mapping the relative file path (from the input directory, using forward slashes) to a dictionary containing:
   - `type`: "file" or "symlink" (record the type of the resolved file).
   - `sha256`: The SHA-256 hex digest of the file's contents.
   - `size`: The file size in bytes.

The final JSON must be pretty-printed with a 2-space indent, and the keys must be sorted alphabetically. 

Please adjust the configuration of the running services if needed to ensure they work together smoothly. Once your script is ready, we will test its behavior extensively.