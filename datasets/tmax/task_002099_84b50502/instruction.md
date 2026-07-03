You are a forensics analyst responding to a compromised Linux host. The threat actor used a custom tool to encrypt and exfiltrate data, as well as receive command-and-control (C2) instructions via web requests. 

We have recovered three pieces of evidence:
1. `/app/c2_session.mp4`: A screen recording of the attacker's terminal session. Somewhere in this video, the attacker sets an environment variable containing the encryption key used for their C2 communication.
2. `/app/c2_crypto.pyc`: A compiled Python 3.10 module recovered from the host. It contains the encryption and decryption routines used by the attacker. 
3. A large dataset of captured web request payloads (not provided directly to you, but will be used to evaluate your solution).

Your objective is to build a classifier/filter that can parse the intercepted web payloads, decrypt them to determine their intent, and either drop malicious C2 payloads or preserve benign traffic.

Perform the following steps:
1. Analyze `/app/c2_session.mp4` to recover the attacker's encryption key. You may use tools like `ffmpeg` and `tesseract` (which are installed).
2. Reverse engineer `/app/c2_crypto.pyc` to understand the encryption algorithm. 
3. Write a Python script at `/home/user/filter.py` with the following CLI signature:
   `python3 /home/user/filter.py --input <input_file> --output <output_file>`
4. The script must read the contents of `<input_file>`, which contains a single encrypted payload.
5. The script must decrypt the payload using the recovered key and the algorithm from `c2_crypto.pyc`.
6. **Classification Rules**:
   - If the decrypted payload contains the exact string `EXFILTRATE` or `C2_EXEC`, it is considered "evil". The script must exit with status code `1` and MUST NOT create the `<output_file>`.
   - If the decrypted payload does not contain those strings, it is considered "clean" (benign encrypted data). The script must copy the *original, unmodified encrypted bytes* from the input file to `<output_file>` and exit with status code `0`.

Your script must be robust and correctly classify 100% of the evaluation corpus, preserving the clean payloads and rejecting the evil ones.