You are a storage administrator managing disk quotas on a Linux server.

You have been provided with a compressed JSON file containing the current disk usage and limits for all users on the system. The file is located at `/home/user/quotas.json.gz`. 

The JSON structure is an array of objects, where each object looks like this:
```json
[
  {"user": "jsmith", "used": 45000, "limit": 50000},
  {"user": "mdoe", "used": 12000, "limit": 50000}
]
```

Your task is to write a robust Bash script at `/home/user/check_quota.sh` that performs the following:
1. Reads the compressed file `/home/user/quotas.json.gz` as a stream (do not decompress it to a file on disk).
2. Parses the JSON data to identify all users who are *strictly* exceeding 90% of their disk quota (`used` > 0.9 * `limit`).
3. Appends the usernames of these users (one per line) to `/home/user/warnings.log`.
4. Because this script will be executed simultaneously by multiple cron jobs in our testing environment, the writing/appending operation **must** be protected by an exclusive file lock. Use `flock` with a lock file at `/home/user/warnings.lock` to ensure concurrent writes do not corrupt the log file.

Requirements:
- Ensure your script is executable (`chmod +x /home/user/check_quota.sh`).
- Do not use temporary files for the parsed data; process the stream directly.
- The output file `/home/user/warnings.log` should only contain the usernames.
- Only output users where the used space is strictly greater than 90% (not equal).

Run your script at least once to verify it works and generates the `/home/user/warnings.log` file.