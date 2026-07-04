You are acting as a security auditor. During a recent internal network review, you discovered a residual authentication script used by the sysadmins to verify permission tokens locally. The original source code was deleted, leaving only a compiled Python bytecode file at `/home/user/checker.pyc`. 

This script is known to contain a hardcoded base64 payload. When provided with a specific 4-character password, the script validates the password using a custom hashing algorithm, derives an XOR key from it, and decodes the payload to yield a highly privileged access token.

Your task is to:
1. Reverse engineer the `/home/user/checker.pyc` bytecode to understand the custom password validation logic and the payload decoding mechanism.
2. Crack or reverse the password (it is exactly 4 ASCII characters).
3. Extract the encoded payload from the bytecode.
4. Decode the payload using the recovered password to obtain the plaintext access token.
5. Save the final, decoded plaintext access token to a new file located exactly at `/home/user/secret.txt`. Do not include any newlines or extra text in this file.

You may use Python and its standard libraries (like `dis` for disassembly) to analyze the bytecode and write your brute-force or decryption scripts.