Act as a DevSecOps engineer enforcing security policies on CI/CD pipelines. We have intercepted several incoming CI/CD webhook payloads that contain build instructions. We suspect some developers might be introducing unauthorized reverse shells or remote execution commands.

Your task is to analyze a batch of JSON webhook payloads located in the directory `/home/user/payloads/`. 

Each JSON file in this directory contains a key named `build_script`. The value of this key is a base64-encoded string representing the shell commands intended to run on our build servers.

Write a Python script (you can save it anywhere, e.g., `/home/user/scanner.py`) to perform the following policy checks:
1. Parse each JSON file in `/home/user/payloads/`.
2. Base64-decode the `build_script` value.
3. Scan the decoded script for any of the following malicious intrusion patterns using regular expressions or substring matching:
   - `nc -e`
   - `curl .* | bash` (this means 'curl' followed by any characters, followed by ' | bash')
   - `wget .* -O- | sh`
4. If a decoded script contains *any* of the malicious patterns, flag the file.
5. For every flagged file, compute the SHA-256 checksum of the **original JSON file** (the exact file bytes, not the decoded content).
6. Output the results to a log file located exactly at `/home/user/flagged_payloads.log`. 

The log file must contain exactly one line per flagged file, sorted alphabetically by filename, in the following format:
`[filename]:[sha256_hash_of_json_file]`

For example:
`payload_02.json:a1b2c3d4e5f6...`

Run your script to generate the log file. Make sure the output format exactly matches the requirements so our automated compliance checker can ingest it.