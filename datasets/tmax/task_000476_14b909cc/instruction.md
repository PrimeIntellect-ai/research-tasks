You are a security auditor testing the perimeter defenses and legacy authentication systems of a secure facility. The facility uses a custom token validation server, but the previous server was compromised and taken offline. Your task is to recover the master authentication token and deploy a secure, sandboxed replacement server in C.

Here are the details of your audit engagement:

1. **Extract the Partial Key (Image Recovery)**
   During a physical walkthrough, an auditor took a photo of an administrator's sticky note, located at `/app/admin_note.png`. You must use OCR tools to extract the text from this image. It contains a partial base key in the format `BASE: <4_characters>`.

2. **Password Cracking / Cryptanalysis**
   The final master token is known to be the 4-character base key followed by exactly two lowercase alphabetic characters (e.g., `a-z`). 
   The facility's documentation states that the MD5 hash of this final 6-character master token is `c4efd5020cb49b9d3257ffa0fbccc0ff`.
   You must implement a brute-force routine in C to discover the correct 2-character suffix that results in this exact MD5 hash.

3. **Secure Auth Server Implementation (C & Process Isolation)**
   Write a C program at `/home/user/secure_auth_server.c` that does the following:
   - Performs the brute-force operation described above to recover the 6-character master token in memory.
   - Starts a TCP server listening on `127.0.0.1:8888`.
   - **Process Isolation:** Immediately after binding the socket, the server must apply process isolation. Specifically, use `seccomp` (via `libseccomp` or standard `prctl`) to explicitly block the `execve` system call to prevent remote code execution vulnerabilities.
   - Accepts incoming raw TCP connections.
   - Reads an incoming token (up to 32 bytes) from the client.
   - If the received token matches the recovered 6-character master token (ignoring trailing newlines), respond with the exact string `GRANTED\n`.
   - If it does not match, respond with `DENIED\n`.
   - Close the client socket after responding and continue listening for new connections.

4. **Deployment**
   Compile your C program (you may use `gcc -o /home/user/secure_auth_server /home/user/secure_auth_server.c -lcrypto -lseccomp` or similar). Run the server in the background so that it is actively listening on port 8888. Keep it running.

You have access to `tesseract-ocr`, `libssl-dev` (for MD5), and `libseccomp-dev` inside the environment.