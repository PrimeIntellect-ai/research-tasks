You are acting as a DevSecOps engineer implementing a custom policy-as-code intrusion detection tool. 

You have been provided with a directory of client certificates, a Root CA, an AES key, and a server log file containing encrypted request payloads. You need to write a C program that processes this log to identify anomalous or malicious requests based on certificate validity and payload contents.

The files are located in `/home/user/`:
- `/home/user/ca.crt`: The Root CA certificate used to verify client certificates.
- `/home/user/certs/`: A directory containing client certificates in PEM format (e.g., `client1.crt`, `client2.crt`).
- `/home/user/secret.key`: A file containing a 32-byte raw binary key used for AES-256-CBC decryption.
- `/home/user/server.log`: A log file where each line represents a request in the following format:
  `<CertFileName> <HexEncodedIV>:<HexEncodedEncryptedPayload>`

Your objective:
1. Write a C program at `/home/user/analyze.c` and compile it to `/home/user/analyze`. Use the OpenSSL library (`libcrypto`, `libssl`) for cryptography and certificate operations.
2. The program must read `/home/user/server.log` line by line.
3. For each line, the program must:
   a. Verify the certificate (located at `/home/user/certs/<CertFileName>`) against the Root CA (`/home/user/ca.crt`). 
   b. Decrypt the payload using AES-256-CBC. The key is in `/home/user/secret.key`. The Initialization Vector (IV) and the encrypted payload are provided in hex-encoded format on the log line.
   c. Perform pattern matching on the decrypted plaintext payload. Flag the request if the payload contains the exact substring `"EXEC_SHELL"`.
4. If a request's certificate fails validation (e.g., self-signed, wrong CA) OR if its decrypted payload contains the `"EXEC_SHELL"` pattern, the program must flag the client.
5. The program should output the names of the flagged certificate files (just the filename, e.g., `client2.crt`), one per line, into a file named `/home/user/flagged.txt` in alphabetical order.

You may install any required development packages (like `libssl-dev` and `gcc`) using local package managers if they aren't already present, assuming standard non-interactive user tools. Once your C program finishes executing, ensure `/home/user/flagged.txt` is written correctly.