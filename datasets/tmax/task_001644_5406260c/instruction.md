You are an incident responder investigating a breach. An attacker has been exfiltrating data and sending malicious XSS and SQL injection payloads to a compromised endpoint, which logs these payloads using a custom, proprietary encryption library left behind on the system.

We have recovered the source code for this custom library, `libmalcrypt-0.5`, located at `/app/libmalcrypt-0.5`. However, the attacker intentionally sabotaged the build environment before abandoning it. 

Your tasks are as follows:
1. **Fix the vendored package**: The `Makefile` in `/app/libmalcrypt-0.5` is broken and fails to compile the shared library. Identify the missing compilation flags or syntax errors, fix the Makefile, and successfully build the library.
2. **Analyze the cipher**: Analyze the C source code of `libmalcrypt-0.5` to understand its custom (and weak) block cipher encryption routine. 
3. **Write a Decoder**: Write a C program at `/home/user/decoder.c` that acts as a standalone decryption tool and log parser. 
   - It must read raw binary data (the encrypted log entries) from `stdin` until EOF.
   - It must decrypt the data using the inverse of the `libmalcrypt` algorithm.
   - The decrypted plaintext consists of URL-encoded key-value pairs (e.g., `timestamp=1234&type=xss&payload=<script>alert(1)</script>`).
   - Your program must parse this plaintext, isolate the value of the `payload` parameter, and print ONLY the raw extracted payload to `stdout`.
   - If the input is invalid or decryption fails the integrity check (if any), print `INVALID` to stdout and exit with code 1.
4. **Compile the Decoder**: Compile your program to an executable located at `/home/user/decoder`.

To ensure your implementation is robust and perfectly reverses the attacker's scheme, we will test your executable `/home/user/decoder` against a secure reference oracle. Your program must produce output that is bit-for-bit identical to our oracle for all possible inputs.