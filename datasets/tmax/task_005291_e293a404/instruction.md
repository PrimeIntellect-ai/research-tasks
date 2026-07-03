You are a storage administrator managing disk space on a legacy logging server. We have a set of old, nested log backups that need to be extracted, validated, transformed, and consolidated to reclaim space.

The legacy system generated multi-part zip archives containing a tar archive, which in turn contains gzip-compressed log files. Some of these gzip archives are corrupted due to disk errors.

Here is your task:
1. Navigate to `/home/user/backups/`. You will find a multi-part zip archive named `archive.zip.001` and `archive.zip.002`. Combine and extract these to get a file named `nested.tar`.
2. Extract `nested.tar` into a directory named `/home/user/extracted/`. Inside, you will find several gzip files (`.tar.gz`).
3. Verify the integrity of these `.tar.gz` files. Discard any archives that are corrupted (fail integrity checks).
4. Extract the valid `.tar.gz` files. Each valid archive contains text-based log files (e.g., `system.log`, `app.log`).
5. Write a Python script at `/home/user/transform.py` that reads raw log lines from `stdin` and writes JSON objects to `stdout` (JSONL format). 
   - The raw log format is: `[YYYY-MM-DD HH:MM:SS] SEVERITY Message`
   - The output JSON format per line should be exactly: `{"timestamp": "YYYY-MM-DD HH:MM:SS", "severity": "SEVERITY", "message": "Message"}`
   - Ignore any lines that do not match this format.
6. Use shell commands (redirection/piping) to concatenate all the extracted `.log` files from the valid archives, pipe them through your Python script (`transform.py`), and save the output to `/home/user/consolidated.jsonl`.
7. Finally, compress the consolidated JSONL file into `/home/user/final_logs.tar.gz` containing only the file `consolidated.jsonl` at the root of the archive.

Do not use root/sudo commands.