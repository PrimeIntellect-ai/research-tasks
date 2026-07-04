You are acting as a storage administrator to reclaim disk space on a legacy system. 

A runaway application has generated a massive, poorly-formatted log file at `/home/user/bloated_log.txt`. The application is currently stopped, but when it restarts, it will demand that this exact file path exists, or it will crash.

Your task is to parse the log to extract valuable usage metrics, save those metrics safely, and then neutralize the bloated log file to reclaim disk space.

Here are the specific requirements:

1. **Log Parsing:** 
   The file `/home/user/bloated_log.txt` is encoded in `UTF-16LE`. It contains multi-line session records. 
   The format looks like this:
   ```
   === SESSION START: <session_id> ===
   [INFO] Processing started
   [TRACE]
     multi-line
     trace output...
   [METRICS] BytesTransferred: <integer>
   === SESSION END ===
   ```
   A single session might have multiple `[METRICS] BytesTransferred: <integer>` lines within its block. You must calculate the total `BytesTransferred` for each `<session_id>`.

2. **Data Export & Atomic Writes:**
   Write a Python script that parses the log and outputs the aggregated byte counts as a JSON dictionary mapping the `session_id` to the total integer bytes transferred (e.g., `{"session_1": 1500, "session_2": 450}`).
   This data must be saved to `/home/user/session_usage.json`. To prevent data corruption in case the system crashes during the write, your Python script **must** write to a temporary file first and then atomically move/replace it to `/home/user/session_usage.json`.

3. **Disk Space Management (Link Management):**
   Once the JSON file is successfully created, delete the original `/home/user/bloated_log.txt` file. Then, to keep the legacy application from filling up the disk again when it restarts, create a symbolic link at `/home/user/bloated_log.txt` that points to `/dev/null`.

Ensure your output JSON matches the parsed metrics exactly, and that the symlink is set up correctly.