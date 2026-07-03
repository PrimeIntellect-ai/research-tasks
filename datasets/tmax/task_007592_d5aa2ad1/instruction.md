You are acting as a storage administrator managing disk space. We have a problem with a faulty log rotation script that was racing with an application's writing process. Because of this race condition, several of our archived log files in `/home/user/logs/` are corrupted. Some are truncated, and others have completely overwritten headers.

Your task is to write a Python script located at `/home/user/cleanup.py` that accomplishes the following:
1. Iterate through all `.tar.gz` files in the `/home/user/logs/` directory.
2. For each file, check if it is a structurally sound gzip compressed tar archive. A file is considered valid ONLY if:
   - It begins with the correct gzip magic number (`1f 8b` in hex).
   - It can be successfully opened and completely read as a tar archive without throwing any integrity exceptions (like `EOFError` or `tarfile.ReadError`).
3. Move all valid archives to the `/home/user/valid_logs/` directory.
4. Move all corrupted or invalid archives to the `/home/user/corrupt_logs/` directory.
5. Create a report file at `/home/user/report.txt` that lists the base filenames (e.g., `log_02.tar.gz`) of all the corrupted archives you found, with one filename per line, sorted in ascending alphabetical order.

Please execute your script and ensure the directories and report are populated correctly. The directories `/home/user/valid_logs/` and `/home/user/corrupt_logs/` already exist.