You are a network security engineer responsible for developing a traffic inspection and archiving tool. You have been given a baseline C++ program, `/home/user/inspector.cpp`, that processes intercepted network request dumps. However, it is currently incomplete, vulnerable to path traversal, lacks sensitive data redaction, does not enforce network policies, and saves files in plaintext.

Your task is to fix the vulnerabilities and implement the missing security features in `/home/user/inspector.cpp`.

Here are the requirements for the C++ program:

1. **Traffic Input**:
   The program takes a single command-line argument: the path to a directory containing intercepted request files (e.g., `/home/user/requests/`). It must process all `.txt` files in that directory.
   Each request file has the following format (always exactly three lines):
   ```
   IP: <IP_ADDRESS>
   Filename: <PROVIDED_FILENAME>
   Body: <PAYLOAD_CONTENT>
   ```

2. **Application-Level Firewall**:
   - Read allowed IP addresses from `/home/user/allowed_ips.txt` (one IP per line).
   - If a request's IP is NOT in this file, reject it.
   - For rejected requests, append a line to `/home/user/firewall.log` in the format: `BLOCKED: <IP_ADDRESS>`, and do not process the file further.

3. **Path Traversal Prevention**:
   - The `Filename` field is vulnerable to path traversal (e.g., `../../../etc/passwd`).
   - Sanitize the filename by extracting only the base name. Strip everything up to and including the last forward slash (`/`) or backslash (`\`). For example, `../folder/secret.txt` becomes `secret.txt`.

4. **Sensitive Data Redaction**:
   - The `Body` often contains sensitive credit card numbers in the format `DDDD-DDDD-DDDD-DDDD` (where `D` is a digit).
   - Before logging or saving the body, redact any such credit card numbers by replacing them exactly with `XXXX-XXXX-XXXX-XXXX`.
   - Append the redacted request details to `/home/user/traffic.log` in the format:
     `[<IP_ADDRESS>] [<SANITIZED_FILENAME>] <REDACTED_BODY>`

5. **Payload Encryption**:
   - Encrypt the *redacted* body using AES-256-CBC.
   - Use the OpenSSL library (`libcrypto`).
   - Use a static 32-byte key consisting of all uppercase 'K's (`KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK`).
   - Use a static 16-byte IV consisting of all uppercase 'V's (`VVVVVVVVVVVVVVVV`).
   - Write the raw binary encrypted payload to `/home/user/uploads/<SANITIZED_FILENAME>.enc`.

**Setup**:
You will need to install the OpenSSL development libraries to compile your C++ code. Use `g++` to compile `/home/user/inspector.cpp` into `/home/user/inspector`. 
Once compiled, run your program against the `/home/user/requests/` directory.

Ensure that the output files (`/home/user/firewall.log`, `/home/user/traffic.log`, and the encrypted files in `/home/user/uploads/`) exactly match the specified formats. Create the `/home/user/uploads/` directory if it does not exist.