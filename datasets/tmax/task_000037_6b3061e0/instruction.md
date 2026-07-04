You are acting as a Security Engineer tasked with rotating credentials and deploying a new token validation filter for our legacy voice-activated API. 

Recently, we initiated a credential rotation. The old master passcode was communicated via a secure voicemail, which has been intercepted and saved at `/app/legacy_passcode.wav`. 

Your objectives are:
1. **Recover the Old Passcode**: Extract the spoken hex passcode from the audio file `/app/legacy_passcode.wav`. (A compiled version of `whisper` or `ffmpeg` is available in the environment to help you transcribe it).
2. **Determine the New Master Seed**: Parse the security logs located at `/app/auth_logs.txt` to find the "Rotation Salt". The *New Master Seed* is the lowercase hex string of the SHA256 hash of the concatenated string: `<old_passcode_from_audio><rotation_salt>`.
3. **Build the Token Filter (C Language)**: Write a C program at `/home/user/token_filter.c` and compile it to `/home/user/token_filter`. This program will act as an adversarial filter for our ingress pipeline.
   The program must accept exactly one argument (the path to a token file) and exit with status code `0` if the token is ACCEPTED, or status code `1` if the token is REJECTED.

**Token Format & Validation Rules:**
Tokens in the files are formatted as: `[Base64_Payload].[Signature]`
*   **Signature Verification**: The `[Signature]` is a 64-character lowercase Hex string representing `SHA256(New_Master_Seed + [Base64_Payload])`. If the signature does not match exactly, REJECT.
*   **Content Security Policy**: Decode the `[Base64_Payload]`. If the decoded payload contains the substrings `<script>`, `javascript:`, or `onload=` (case-insensitive), REJECT.
*   **Legacy Block**: If the signature matches the old master passcode instead of the new one, REJECT.
*   If the token is perfectly formatted, signed with the *New* Master Seed, and contains a safe payload, ACCEPT.

**Testing:**
You have access to a clean corpus and an evil corpus:
*   `/app/corpus/clean/` contains valid, safe tokens.
*   `/app/corpus/evil/` contains forged tokens, malicious XSS payloads, and legacy tokens.
Your compiled `/home/user/token_filter` must perfectly classify these files. Use standard C libraries and OpenSSL (`-lssl -lcrypto`) for your implementation.