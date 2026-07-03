You are a DevSecOps engineer enforcing policy as code in a CI/CD pipeline. Your team has a system that produces logs in JSON format, but some of these logs mistakenly contain AWS Access Key IDs. Furthermore, the log processing must be run in a network-isolated environment to prevent any accidental exfiltration of data.

You have a raw log file located at `/home/user/raw_logs.json`. The file contains a JSON array of objects, where each object has an `id` and a `b64_payload` (a base64-encoded UTF-8 string).

Your task is to write a Python script at `/home/user/enforce.py` that does the following:
1. Reads `/home/user/raw_logs.json`.
2. Iterates over each log entry and decodes the `b64_payload`.
3. Redacts any AWS Access Key IDs found in the decoded string. An AWS Access Key ID is defined as any string starting with `AKIA` followed by exactly 16 uppercase alphanumeric characters (Regex: `AKIA[A-Z0-9]{16}`).
4. Replaces the exact match of the key with the string `[REDACTED]`.
5. Re-encodes the redacted string back to base64.
6. Writes the resulting JSON array to `/home/user/clean_logs.json` using the exact same structure as the input.

After writing the script, you must execute a command that takes the output from `/home/user/clean_logs.json` and writes it to `/home/user/final_output.log`, but you must use the `unshare` command to isolate the process. Specifically, use `unshare` to run a bash command (`cat /home/user/clean_logs.json > /home/user/final_output.log`) in a new user and network namespace (no network access). 

You should perform the entire execution so that `/home/user/final_output.log` is successfully created with the redacted data.