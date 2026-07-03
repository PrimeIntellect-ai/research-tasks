You are a forensics analyst investigating a compromised Linux host. We suspect an attacker exploited a path traversal vulnerability in a custom C-based file upload handler to hide an encrypted payload on the system.

You have been provided with the following artifacts in `/home/user/investigation/`:
1. `upload_handler.c`: The source code of the vulnerable upload service. 
2. `access.log`: The HTTP request logs leading up to the incident.

Your objective is to locate, decrypt, and recover the hidden evidence. 

Here is what we know about the attacker's methodology:
- They bypassed the upload directory restriction via path traversal in the `filename` parameter (URL-encoded).
- They encrypted the payload using a repeating-key XOR cipher.
- The encryption key is derived by concatenating a session token found in the attacker's HTTP `Cookie` header (from the malicious POST request in the log) with a 4-digit numeric PIN (e.g., if the cookie is `session=XY12`, the key might be `XY120000` through `XY129999`).
- The decrypted plaintext of the payload is known to strictly begin with the string: `EVIDENCE{`

Your tasks:
1. Analyze `access.log` to identify the malicious file upload request, the path traversal filename, and the session cookie.
2. Determine the exact absolute path where the attacker's payload was saved (the server's intended upload directory is `/home/user/investigation/uploads/`, but the path traversal modifies this).
3. Write a C program at `/home/user/investigation/recover.c` that reads the encrypted payload, brute-forces the 4-digit PIN appended to the session cookie, and decrypts the payload.
4. Run your C program and write the successfully decrypted plaintext to `/home/user/recovered_evidence.txt`.

Ensure the recovered evidence file contains only the decrypted string.