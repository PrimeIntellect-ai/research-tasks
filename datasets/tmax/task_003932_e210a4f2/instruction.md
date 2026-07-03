You are a security engineer tasked with securing a voice-based credential rotation system. The legacy system has been vulnerable to privilege escalation and command injection (CWE-77, CWE-22) due to improper handling of audio file paths and transcripts. 

Your objective is to write a standalone C program, `filter.c`, that validates incoming credential rotation requests and compiles to `/home/user/filter`.

Here are the requirements:
1. **Current Passphrase Extraction**: A sample of the current valid authentication audio is located at `/app/auth_sample.wav`. You must transcribe this audio file to recover the spoken passphrase. This passphrase must be used in your filter; any rotation request that does not include this exact passphrase as the `old_passphrase` field must be rejected.
2. **Request Validation**: The system receives rotation requests in a simple text format on Standard Input (stdin). Each request has the following format (one key-value pair per line):
   ```
   file_path: <path_to_audio_file>
   old_passphrase: <transcribed_text>
   new_passphrase: <new_text>
   file_sha256: <hex_encoded_sha256_of_the_audio_file>
   ```
3. **Security Filtering (Adversarial Robustness)**: 
   - You must identify and reject requests attempting to exploit command injection or path traversal vulnerabilities in the `file_path` field (e.g., containing characters like `;`, `|`, `&`, `$`, `..`).
   - You must reject requests where the `file_path` does not end in `.wav`.
   - You must reject requests where the `old_passphrase` does not exactly match the transcript of `/app/auth_sample.wav`.
   - You must reject requests where the `file_sha256` is not exactly 64 hexadecimal characters.
4. **Behavior**: 
   - If a request is completely safe and valid, your program must exit with status code `0` (Accept).
   - If a request violates any security rules or contains an incorrect old passphrase, your program must exit with status code `1` (Reject).

Compile your code using: `gcc -O2 /home/user/filter.c -o /home/user/filter`

Ensure your C program strictly reads from stdin and returns the appropriate exit code. You may use any available tools (like ffmpeg or whisper) in the terminal to analyze `/app/auth_sample.wav` before writing your C code.