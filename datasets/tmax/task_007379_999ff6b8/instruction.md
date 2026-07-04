You are a backup administrator recovering data from a legacy server. You have been given a set of backup archives in `/home/user/backups/`. Some of these archives were corrupted during transit.

Your task is to:
1. Verify the integrity of the gzip-compressed tar archives in `/home/user/backups/` to find the single valid archive. 
2. Extract the file `server.log` from the valid archive.
3. The `server.log` file is encoded in `UTF-16LE`. It contains multi-line log records that begin with a tag (e.g., `[INFO]`, `[ERROR]`) on its own line and end with a matching closing tag (e.g., `[/INFO]`, `[/ERROR]`) on its own line.
4. Extract all complete multi-line error records (everything from `[ERROR]` to `[/ERROR]`, inclusive).
5. Convert the extracted text to `UTF-8` encoding.
6. Append these UTF-8 encoded error records to `/home/user/critical.log`. 
7. **Crucial:** You must acquire an exclusive file lock on `/home/user/critical.log` while appending to it (for example, using the `flock` command or programmatic file locking like Python's `fcntl`). A background process monitors this file and strict locking is required to prevent data corruption.

Ensure your final `/home/user/critical.log` contains only the `UTF-8` encoded error records, exactly as they appeared in the source file but in the new encoding.