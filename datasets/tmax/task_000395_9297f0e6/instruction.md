You are acting as a penetration tester analyzing artifacts recovered from a compromised server. You suspect the attacker has tampered with some of the stored payloads to inject malicious shellcode, bypassing the application's native integrity checks.

The artifacts are stored in the directory `/home/user/artifacts/`. 
Each file in this directory follows a strict format:
```
Encoding: base64
Checksum: <sha256_hex_digest>
Payload: <base64_encoded_string>
```

Your objective is to write a Python script at `/home/user/scanner.py` that processes every file in `/home/user/artifacts/` to verify their cryptographic integrity. 

For each file, your script must:
1. Extract the `Checksum` and `Payload` strings.
2. Decode the `Payload` from base64 into its raw bytes.
3. Calculate the SHA-256 hash of the decoded raw bytes.
4. Compare the calculated hash against the provided `Checksum`. 
5. If the calculated hash DOES NOT match the provided checksum, the file is considered "tampered".

After evaluating all files, your script must generate a log file at `/home/user/tampered.log`. 
The log file must contain one line for each tampered file, sorted alphabetically by the filename. Each line must be formatted exactly as follows:
`<filename>:<hex_encoded_decoded_payload>`

For example, if `artifact_9.txt` was tampered and its decoded payload was the string `id`, the line would be:
`artifact_9.txt:6964`

Run your script to produce the final `/home/user/tampered.log` file. You may only use Python standard libraries.