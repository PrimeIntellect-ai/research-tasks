You are a network security engineer investigating a series of breaches targeting a legacy authentication daemon. Attackers have been injecting malicious payloads that result in privilege escalation and credential leakage via command-line arguments visible in `/proc`. 

To mitigate this, you must write a strict payload filter in C that acts as a local application-layer firewall. This filter will be deployed as an inspection hook to validate incoming authentication tokens.

A screenshot of the legacy daemon's architectural specification is located at `/app/auth_spec.png`. You must extract the `SECRET_KEY` and the list of `RESTRICTED_STRINGS` from this image.

Your task is to create a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.

### Payload Format
Incoming payloads are stored in text files. The file contains a single continuous Hexadecimal string (uppercase or lowercase, no newlines or spaces).
Once the Hex string is decoded into raw binary, the payload is structured as follows:
1. The first 32 bytes represent a SHA-256 signature.
2. The remaining bytes represent the `Data` payload (an ASCII string).

### Validation Rules
Your filter must validate the payload based on the following rules. If ANY rule is violated, the program must reject the payload by exiting with **exit status 1**. If all rules pass, the program must accept the payload by exiting with **exit status 0**.

1. **Decoding:** The file must contain valid hex-encoded data.
2. **Length:** The decoded binary data must be strictly greater than 32 bytes.
3. **Signature Validation:** The 32-byte signature must exactly match the SHA-256 hash of the `Data` concatenated with the `SECRET_KEY` (i.e., `SHA256(Data || SECRET_KEY)`).
4. **Security Auditing:** The decoded `Data` (ASCII string) MUST NOT contain any of the `RESTRICTED_STRINGS` defined in the specification image.

### Corpora & Verification
We have captured network traffic and categorized it into two directories:
- `/app/corpus/clean/`: Contains 50 known-good payloads that must be accepted.
- `/app/corpus/evil/`: Contains 50 malicious payloads that must be rejected.

Your compiled program (`/home/user/filter`) will be executed against these corpora as follows:
`./filter /app/corpus/clean/payload_01.txt`
`./filter /app/corpus/evil/payload_01.txt`

You must ensure that your filter achieves a 100% acceptance rate on the clean corpus and a 100% rejection rate on the evil corpus. You are encouraged to install any necessary C libraries (e.g., `libssl-dev`) and use standard command-line tools (e.g., `tesseract-ocr` or `imagemagick`) to aid your development and analysis.