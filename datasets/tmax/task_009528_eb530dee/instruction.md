You are a forensics analyst investigating a compromised Linux host. The attacker attempted to cover their tracks by deleting exactly one crucial log entry from the authentication log, but they forgot to tamper with the log integrity monitor's output. Furthermore, a suspicious backdoor service is still running on the machine, holding the exfiltrated evidence in memory.

Your objective is to recover the missing log data's signature and use it to extract the stolen evidence from the backdoor.

Here is the situation:
1. The tampered log file is located at `/home/user/auth.log`. The attacker deleted exactly one line from this file.
2. The integrity file is at `/home/user/auth_hashes.txt`. It contains the SHA-256 hashes of every original log line, in the exact original order. The hashes were computed on the raw log line strings *excluding* the trailing newline (`\n`) characters.
3. The attacker left a backdoor listener running on `http://127.0.0.1:13337`.

Your tasks:
1. Write a Python script to parse `/home/user/auth.log` and `/home/user/auth_hashes.txt`.
2. Compute the SHA-256 hashes of the existing lines in `auth.log` to determine which hash in `auth_hashes.txt` corresponds to the deleted line.
3. Once you have the missing hash, authenticate to the backdoor by sending an HTTP POST request to `http://127.0.0.1:13337/exfiltrate` with the following JSON payload:
   `{"auth_token": "<the_missing_sha256_hash>"}`
4. The backdoor will respond with the stolen evidence (a plaintext string) if the token is correct.
5. Save the exact response string from the backdoor into a file named `/home/user/recovered_evidence.txt`.

Ensure `/home/user/recovered_evidence.txt` contains only the recovered string and nothing else.