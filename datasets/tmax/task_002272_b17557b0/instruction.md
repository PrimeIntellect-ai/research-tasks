You are acting as a storage administrator for a high-performance computing cluster. Recently, a runaway backup script created a massive tangled web of recursive symlinks, corrupted archives, and bloated text logs, threatening our disk space.

We have a screen recording of the cluster monitoring dashboard during the incident, located at `/app/system_incident.mp4`. You must extract frames from this video to identify the specific error code (a 5-character alphanumeric string) that was flashing on the screen during the critical failure window (between 00:02 and 00:05). 

Your objective is to write a Python script, `/home/user/storage_cleaner.py`, that acts as a robust filesystem filter. This script must process a given target directory, performing the following tasks safely:
1. **Recursive Traversal & Symlink Safety**: Traverse the directory. If a symlink points to an ancestor directory (causing an infinite loop), it must be unlinked and logged.
2. **Archive Verification**: Identify all `.zip` and `.tar.gz` files. Verify their integrity. Corrupted archives must be deleted.
3. **Log Sanitization**: Identify all `.log` files. Scan them for the specific error code you found in the video. If the error code is found, the file must be modified to replace all occurrences of the error code with the string `[REDACTED]`. You must use atomic writes (write to a temporary file, then rename) to ensure no logs are left in an incomplete state if interrupted.

The script must accept a single command-line argument: the path to the directory to process.
`python3 /home/user/storage_cleaner.py <directory_path>`

To prove your script works, it will be evaluated against two pre-existing directory structures:
- `/app/corpora/clean/`: Contains valid archives, safe symlinks, and normal logs. Your script must leave this directory functionally identical (valid files untouched, valid logs unredacted since they lack the error code).
- `/app/corpora/evil/`: Contains recursive symlinks, corrupted archives, and logs filled with the error code. Your script must sanitize this directory entirely (removing bad symlinks, deleting bad archives, redacting logs).

Please write the script. You can use standard Python libraries. `ffmpeg` is available for video processing.