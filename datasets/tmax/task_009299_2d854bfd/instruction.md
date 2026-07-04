You are assisting a storage administrator with managing disk space on a busy server. We have several active log files that are constantly being written to. We need a robust Bash script that safely archives these logs, compresses them, and generates a checksum manifest without losing any data to race conditions.

Please create a Bash script at `/home/user/archive_worker.sh`. The script must meet the following precise specifications:
1. It must accept exactly one argument: the full path to a log file.
2. It must open the target log file for both reading and writing, and acquire an exclusive lock on it using `flock` to ensure no other process writes to it while archiving.
3. It must read the uncompressed contents of the file exactly once. Using standard stream redirection, piping, and process substitution, it must simultaneously:
   - Compress the stream using `gzip` and save it to `/home/user/archived_logs/<basename>.gz` (where `<basename>` is the name of the log file, e.g., `web.log.gz`).
   - Calculate the SHA-256 checksum of the *uncompressed* data.
4. While still holding the lock on the original log file, it must truncate the original log file to 0 bytes (clearing it for new logs).
5. It must safely append the checksum and the base filename to `/home/user/archived_logs/manifest.txt` in the standard format (e.g., `d2d2...  web.log`). Because multiple workers might write to the manifest concurrently, the script MUST acquire an exclusive `flock` on the manifest file before appending to it.

After you have written and made `/home/user/archive_worker.sh` executable, manually run it on the following three existing files to perform the archiving:
- `/home/user/active_logs/web.log`
- `/home/user/active_logs/db.log`
- `/home/user/active_logs/auth.log`

Verify that the `.gz` files are created, the original files are 0 bytes, and the manifest contains the correct entries.