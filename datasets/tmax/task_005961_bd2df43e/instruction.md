You are a forensics analyst investigating a compromised Linux host. You have discovered a suspicious log file and an encrypted archive left behind by the attacker.

Your objectives:
1. Analyze the log file located at `/home/user/c2_traffic.log`. It contains base64-encoded payloads. Decode these payloads to find a clue about the encryption password for the archive.
2. The archive is located at `/home/user/evidence.zip`. Use the clue from the decoded payloads to brute-force or determine the password and extract its contents.
3. Inside the extracted archive, you will find a TLS certificate file named `server.crt`.
4. Parse the certificate to extract the Subject's Common Name (CN).
5. Save exactly the Common Name (just the value, no extra text) to a file at `/home/user/cn.txt`.

You must use Python or bash commands to complete these steps. The primary goal is to produce `/home/user/cn.txt` containing the correct CN.