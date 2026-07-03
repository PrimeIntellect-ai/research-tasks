You are a storage administrator managing backups and disk space. You have received an archive (`/home/user/backups/data.tar`) that might contain potentially malicious paths (e.g., directory traversal/zip slip attempts). 

Your task is to write a Python script `/home/user/safe_extract.py` that securely extracts tar archives, and then run it to extract `/home/user/backups/data.tar` into `/home/user/extracted`.

Your script must be invoked as:
`python3 /home/user/safe_extract.py <tar_file_path> <target_directory_path>`

The script must fulfill the following requirements:
1. **Prevent Zip Slip**: It must safely extract files. Any file in the archive whose destination resolves to a path strictly outside the `<target_directory_path>` must be completely ignored. The script must log the exact archive member name of these skipped files to `/home/user/skipped.log` (one member name per line).
2. **Incremental Extraction**: To save disk I/O, only extract a file if it does not already exist in the target directory, OR if the archive member's modification time (mtime) is strictly greater than the existing file's mtime on disk.
3. **Concurrency Control**: Before beginning the extraction, the script must acquire an exclusive file lock using `fcntl.flock` on a lock file named `.extract.lock` located inside the `<target_directory_path>`. The lock should be released when extraction is complete. Create the lock file if it doesn't exist.
4. **Encoding Conversion**: The legacy system that generated the backups used `ISO-8859-1` encoding for text files. Whenever your script successfully extracts a file ending in `.txt`, it must read the newly extracted file as `ISO-8859-1` and overwrite it in place as `UTF-8`.

Once your script is complete, run it:
`python3 /home/user/safe_extract.py /home/user/backups/data.tar /home/user/extracted`