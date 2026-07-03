You are acting as a log analyst investigating patterns across multiple system components.

You have been given two log files located in `/home/user/logs/`:
1. `server.log` - Contains connection statuses.
   Format: `[YYYY-MM-DD HH:MM:SS] IP: <ip_address> STATUS: <code>`
2. `app.log` - Contains application actions.
   Format: `[YYYY-MM-DD HH:MM:SS] USER: <username> IP: <ip_address> ACTION: <action>`

Your objective is to write a Python script at `/home/user/analyze.py` that processes these logs and generates a stratified sample of the correlated events. 

Specifically, your script must:
1. Parse both log files. You should use regular expressions to cleanly extract the timestamp (as a single string), IP address, status code, username, and action.
2. Join the two datasets on exact matches of both `timestamp` and `ip_address`.
3. Perform a stratified sample on the joined data based on the `STATUS` code:
   - For each unique `STATUS` code, select a maximum of 2 records.
   - If there are more than 2 records for a given status, select the 2 with the earliest timestamps.
4. Output the final sampled data to `/home/user/output.json` as a JSON array of objects.
   - Each object must have exactly these keys: `"timestamp"`, `"ip"`, `"status"`, `"user"`, `"action"`.
   - The array must be sorted chronologically by `"timestamp"`.

Run your script to ensure `/home/user/output.json` is created with the correct format and data.