You are an incident responder investigating a potential data breach. You have discovered a suspicious stripped binary at `/app/token_processor` that the attackers left behind. It appears to be a custom tool used to generate and validate proprietary authentication tokens found in the compromised system's logs.

We have a massive log file of these tokens at `/home/user/incident_logs.txt`. Each line contains a single base64-encoded token.

Your task is to:
1. Analyze the `/app/token_processor` binary to understand how it encrypts/decrypts and validates these tokens. It is known to use a symmetric encryption algorithm and a custom signature generation method. 
2. Write a C++ program at `/home/user/analyze_tokens.cpp` that reads `/home/user/incident_logs.txt`.
3. For each token, your C++ program must:
   a. Decrypt the token payload.
   b. Validate the signature (the binary has a flaw similar to the "alg=none" JWT vulnerability where certain modified headers bypass signature checks; you must properly implement the *intended* strict validation and reject forged tokens).
   c. If the token is valid, parse the decrypted payload (which is in JSON format).
   d. Redact any sensitive data: specifically, replace the values of the keys `"ssn"` and `"credit_card"` with the exact string `"[REDACTED]"`.
   e. Output the valid, redacted JSON payloads, one per line, to `/home/user/clean_logs.jsonl`.
4. Compile your C++ program and run it to produce `/home/user/clean_logs.jsonl`.

Note: You have `gdb`, `objdump`, `strace`, and standard C++ compilation tools available. The performance and accuracy of your C++ tool will be evaluated.