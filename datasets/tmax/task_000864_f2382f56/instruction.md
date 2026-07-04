You are a forensics analyst investigating a compromised Linux host. The attacker exploited an open redirect vulnerability in a custom Go web application to steal an administrator's session cookie. Using that hijacked session, they exfiltrated sensitive data. 

Before exfiltrating the data, the attacker encrypted it and left a copy of the encrypted blob on the server at `/home/user/exfiltrated.enc`. 

We also recovered the web server logs at `/home/user/access.log`.

Through reverse-engineering the attacker's toolkit (not included here), we know the following about their encryption scheme:
1. They used AES-256-GCM.
2. The standard Go implementation was used, meaning the encrypted file consists of a 12-byte nonce followed by the ciphertext (which includes the 16-byte GCM authentication tag at the end).
3. The AES key is a SHA-256 hash of a specific string: a 4-digit PIN appended directly to the hijacked `session_id` value (e.g., if the PIN is `1234` and the session_id is `abc`, the key is `SHA256("1234abc")`).

Your task is to:
1. Inspect `/home/user/access.log` to identify the open redirect attack and extract the hijacked `session_id` value. The open redirect payload points to an external domain `attacker.com`.
2. Write a Go program at `/home/user/decrypt.go` that brute-forces the 4-digit PIN (from `0000` to `9999`).
3. Your Go program must derive the correct AES key, decrypt the contents of `/home/user/exfiltrated.enc`, and write the decrypted plaintext flag to `/home/user/recovered.txt`.

Ensure your Go program correctly parses the 12-byte nonce from the beginning of the encrypted file before attempting decryption. The final decrypted text must be written exactly as-is to `/home/user/recovered.txt` with no additional text or formatting.