You are acting as a penetration tester analyzing a sophisticated web shell left behind by an APT group. We have recovered a few artifacts from the compromised server, but we need you to build a reliable payload decoder to understand the attacker's actions.

Here is what we know:
1. The attacker left behind an image at `/app/secret_key.png` which contains the master decryption key in plain text (use OCR to extract it).
2. The web shell communicates via HTTP GET requests logged in standard format. The malicious payload is always passed in the `?token=` URL parameter as a Base64-encoded string.
3. The attacker restricts access to the web shell using Mutual TLS. The log line contains the Client Certificate Serial Number in a custom header `X-Client-Serial`. 
4. We have a directory of valid client certificates at `/app/certs/` in PEM format.

Your task is to write a Python 3 script at `/home/user/decode_payload.py` that takes a single Apache access log line as a command-line argument and does the following:
1. Parse the log line to extract the `token` parameter and the `X-Client-Serial` value.
2. Verify that a certificate with that exact serial number (in hexadecimal) exists and is valid (not expired) within the `/app/certs/` directory.
3. If the certificate is invalid or missing, print `AUTH_FAILED` to stdout and exit.
4. If valid, Base64-decode the `token` payload.
5. The decoded payload consists of a 16-byte IV followed by the AES-128-CBC encrypted command.
6. Decrypt the command using the key extracted from `/app/secret_key.png`.
7. Print the decrypted command (as a UTF-8 string) to stdout.

We have a compiled reference binary at `/app/oracle_decoder` that performs this exact extraction, but it's obfuscated and we need your Python source code for further analysis. Your script must be bit-exact equivalent to the oracle in its stdout output for any given log line. 

Ensure your script handles exceptions gracefully and outputs `ERROR` if the log line is malformed or decryption fails.