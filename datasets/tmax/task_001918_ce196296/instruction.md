You are a network security engineer investigating a suspected data exfiltration incident. A compromised internal server appears to be sending covert traffic to external C2 (Command and Control) servers via custom HTTP headers.

You have been provided with two files:
1. `/home/user/traffic.json` - A JSON file containing an array of logged HTTP requests.
2. `/home/user/cert.pem` - An X.509 certificate found on the compromised server.

Your investigation reveals the following about the attacker's methodology:
- The attacker hides encrypted data in the `X-Telemetry-Data` HTTP header of outgoing requests.
- The data in this header is Base64 encoded.
- Once Base64 decoded, the first 16 bytes represent the Initialization Vector (IV). The remainder of the data is the ciphertext.
- The ciphertext is encrypted using AES-128 in CBC mode with PKCS7 padding.
- The 16-byte AES decryption key is hidden inside the provided X.509 certificate (`/home/user/cert.pem`). Specifically, the key is the exact string value of the `Organization Name` (O) attribute in the certificate's `Subject`.

Your task:
1. Extract the decryption key from the X.509 certificate.
2. Inspect the HTTP requests in `/home/user/traffic.json`.
3. For every request containing an `X-Telemetry-Data` header, extract, decode, and decrypt the payload.
4. Scan the decrypted plaintext for the intrusion detection signature: `[C2_EXFIL_START]`.
5. Identify the `src_ip` (Source IP) of every request where the decrypted payload contains this signature.
6. Write the unique, strictly ascending sorted list of these malicious source IPs to a log file at `/home/user/malicious_ips.txt`. Each IP must be on a new line.

Requirements:
- Write a Python script to automate this analysis.
- You may use the `cryptography` Python library, which you can install via pip if it's not present.
- Save the final result exactly at `/home/user/malicious_ips.txt`.