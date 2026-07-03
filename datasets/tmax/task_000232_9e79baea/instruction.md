You are a penetration tester tasked with analyzing a proprietary authentication service that was recently breached. We have two artifacts from the incident: a screen recording of the server's debug console and a stripped binary used for generating cookie signatures.

**Phase 1: Video Analysis and Data Redaction**
We recovered a screen recording of the server's console at `/app/network_traffic.mp4`. This console prints raw HTTP headers and cookies of incoming requests in real-time. 
1. Extract and analyze the frames of this video to inspect the HTTP headers.
2. Locate the single HTTP request that contains the header `X-Exploit-Payload: true`.
3. From that specific request, extract the value of the `Session-ID` cookie.
4. Redact this sensitive session ID: keep only the first 4 characters of the cookie value in plaintext, and replace the entire rest of the string with exactly 8 asterisks (e.g., if the cookie was `supersecret`, it becomes `supe********`).
5. Save this redacted string to exactly `/home/user/redacted_session.txt` (the file should contain only this string and a newline).

**Phase 2: Reverse Engineering and Algorithm Replication**
The service uses a proprietary hashing algorithm to validate these `Session-ID` cookies. We have recovered the stripped utility used to generate these hashes at `/app/auth_oracle`.
1. Analyze and reverse engineer the `/app/auth_oracle` ELF binary to understand its custom hashing logic. The binary takes a single string as a command-line argument and prints the resulting hash in hex format to standard output.
2. Write your own implementation of this hashing algorithm. You may use any language (Python, C, Node.js, etc.), but the final executable must be located at `/home/user/hash_generator`.
3. Ensure `/home/user/hash_generator` is marked executable (`chmod +x`). If it is a script, include the appropriate shebang. If it is a compiled language, compile the binary to this exact path.
4. Your program must take exactly one command-line argument (the input string) and output the exact same string as `/app/auth_oracle` to stdout. 
5. Your implementation will be rigorously tested against the oracle using thousands of randomly generated fuzzing inputs to ensure bit-exact equivalence.

Do not attempt to wrap or call `/app/auth_oracle` in your script; you must implement the algorithm from scratch. Your final submission must contain the redacted session file and the executable generator.