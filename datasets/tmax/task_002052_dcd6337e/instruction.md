You are acting as a penetration tester and security developer. You have intercepted a server administrator dictating a secret passphrase. The recording is located at `/app/interception.wav`.

Your task is to securely implement a custom file-upload TCP service in C that authenticates requests using this passphrase, while ensuring it is immune to path traversal attacks.

Step 1: Recover the Passphrase
Transcribe the spoken audio in `/app/interception.wav`. The spoken content is a sequence of lowercase English words separated by a single space. This exact string (without leading/trailing whitespace or punctuation) is your `PASSPHRASE`.

Step 2: Implement the Secure Upload Service in C
Create a C program that acts as a TCP server listening on `127.0.0.1:8080`.
The server must handle incoming TCP connections using the following line-based text protocol (each line terminated by `\n`):

```
FILENAME <filename>
HASH <sha256_hex>
PAYLOAD <base64_encoded_data>
```

For each connection, the server must:
1. Parse the three lines.
2. Decode the base64 payload.
3. Compute the SHA256 hex digest of the decoded bytes concatenated with the `PASSPHRASE`. (For example, if the decoded payload is `test` and passphrase is `alpha beta`, compute the SHA256 of `testalpha beta`).
4. Validate that the computed hash strictly matches the provided `<sha256_hex>`.
5. Write the decoded payload bytes to `/home/user/uploads/<filename>`.
6. Return exactly "OK\n" to the client and close the connection on success.
7. Return exactly "ERROR\n" to the client and close the connection on any failure (parsing error, base64 error, hash mismatch, or security violation).

Step 3: Prevent Vulnerabilities
The server must be explicitly protected against Path Traversal. If the `<filename>` contains any `/` or `..`, the server must immediately return "ERROR\n", close the connection, and discard the payload without writing any files.

Step 4: Logging
Whenever a file is successfully written, append a line to `/home/user/server.log` in the exact format:
`Written: <filename>`

Step 5: Deployment
Compile your C program, ensure the directory `/home/user/uploads` exists, and start your server in the background so it is listening on `127.0.0.1:8080`. Leave it running. We will test it using an automated verification script that will connect to the port, send various valid, invalid, and malicious (path traversal) payloads, and check the server's responses and the state of `/home/user/uploads`.