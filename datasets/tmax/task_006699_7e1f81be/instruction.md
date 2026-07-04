You are acting as a network security engineer investigating a recent spike in suspicious file upload traffic. You have been provided with an extracted log file from the upload service.

The log file is located at `/home/user/upload_requests.log`.
Each line in this log file represents an upload request and is formatted as three space-separated columns:
`[TIMESTAMP] [IP_ADDRESS] [BASE64_ENCODED_FILEPATH]`

Your task is to:
1. Parse the log file and extract the base64-encoded payloads (the third column).
2. Decode each payload to reveal the requested destination file path.
3. Identify the specific decoded file path that is attempting a path traversal attack (specifically, look for a path containing the sequence `../`).
4. Write the exact decoded string of the malicious file path to a new file at `/home/user/malicious_payload.txt`. Do not include a trailing newline if the decoded payload didn't have one, but standard echo with bash command substitution is fine (the base64 decoded string itself does not contain a newline).
5. Set the file permissions of `/home/user/malicious_payload.txt` to strictly `600` (read and write for the owner only).
6. Verify the integrity of your finding by computing the SHA256 checksum of `/home/user/malicious_payload.txt` and saving the entire output of the `sha256sum` command to `/home/user/payload_hash.txt`.

Ensure all file paths and permissions exactly match the instructions. Use standard Linux utilities to complete this task.