You are acting as a security auditor reviewing a system's configuration. During your audit in `/home/user`, you have uncovered two security issues that need your immediate attention.

**Part 1: Code Auditing & Content Security Policy (CSP)**
You found a simple Go web server script located at `/home/user/server.go`. Upon reviewing it, you identified a CWE-693 (Protection Mechanism Failure) vulnerability: it serves HTML content but lacks a Content-Security-Policy header to mitigate XSS attacks.
Your task is to fix this script. Modify the code to include the following HTTP response header:
`Content-Security-Policy: default-src 'self'; script-src 'none';`
Save your corrected version of the server script to `/home/user/server_fixed.go`. Do not change the existing body of the HTTP response.

**Part 2: Password Cracking & Decryption**
You also found an encrypted backup file at `/home/user/secrets.enc` and a corresponding dictionary file at `/home/user/wordlist.txt`. 
The file `secrets.enc` was encrypted using AES-256-GCM. The encryption scheme is as follows:
- The 256-bit AES key is the SHA-256 hash of the plaintext password.
- The first 12 bytes of `secrets.enc` contain the randomly generated GCM nonce.
- The rest of the file is the ciphertext (which includes the GCM auth tag at the end, standard for Go's `crypto/cipher` AES-GCM implementation).

You must write a Go script (e.g., `/home/user/cracker.go`) to brute-force the decryption of `secrets.enc` using the passwords in `wordlist.txt`. 
Once you successfully decrypt the file, write the exact decrypted plaintext string into `/home/user/decrypted_secret.txt` (without any trailing newlines unless they are part of the decrypted string).

Verify your work by ensuring `/home/user/server_fixed.go` contains the proper header enforcement and `/home/user/decrypted_secret.txt` contains the recovered secret.