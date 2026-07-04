You are acting as a forensics analyst investigating a compromised Linux host. We have discovered a custom authentication binary used by the web application, located at `/app/auth_svc` (a stripped, statically linked ELF binary). 

Initial analysis shows that the application uses a custom token format similar to JWT, typically passed in the `Authorization` HTTP header. The attacker managed to forge tokens to gain administrative access. We suspect there is a logic flaw or backdoor in how the binary validates tokens (e.g., handling of specific algorithms or missing signature checks).

Your tasks are to:
1. Reverse engineer `/app/auth_svc` to understand its token parsing and validation logic, specifically identifying the vulnerability the attacker used to bypass authentication.
2. Write a Python script at `/home/user/detector.py` that acts as a classifier and sanitiser for these tokens. 

The script must have the following CLI signature:
`python3 /home/user/detector.py <input_token_file> <output_token_file>`

- The script should read a file containing one base64-encoded token per line.
- It must inspect the token's unencrypted headers/payload (like HTTP header inspection).
- If the token is "clean" (properly formed, uses the standard HMAC-SHA256 signature, and does not exploit the bypass), the script should write it to the output file exactly as is.
- If the token is "malicious" (exploits the vulnerability you found in the binary), the script MUST reject it by writing a redacted version to the output file. The redacted version should replace the entire token payload with the string `[MALICIOUS_TOKEN_REDACTED]`.

Ensure your script is robust and properly handles base64 padding and JSON decoding. The script will be tested against a large corpus of collected logs.