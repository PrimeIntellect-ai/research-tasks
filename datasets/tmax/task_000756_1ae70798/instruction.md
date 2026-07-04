You are a network security engineer investigating an open redirect vulnerability in a legacy authentication service. You have intercepted an audio recording of a telecom transmission that contains the backup secret key used to sign redirect tokens, transmitted as a sequence of DTMF (Dual-Tone Multi-Frequency) tones.

Your task is to decode the intercepted key and implement a secure token validator in Python to replace the vulnerable legacy component.

1. **Extract the Secret Key**:
   Analyze the audio file located at `/app/dtmf_intercept.wav`. It contains a sequence of DTMF tones representing digits. This sequence of digits (as an ASCII string) is the secret HMAC key.

2. **Implement the Token Validator**:
   Write a Python 3 script at `/home/user/redirect_handler.py` that takes a single hex-encoded string (the token) as its only command-line argument. The script must decode the hex string and parse the custom binary format to validate the token and enforce a strict URL security policy.

   **Token Binary Format (Post-Hex Decode)**:
   - Bytes 0-3: Magic bytes `REDI` (ASCII).
   - Bytes 4-5: Length of the URL (unsigned 16-bit integer, big-endian).
   - Bytes 6 to `6 + Length - 1`: The URL string (ASCII).
   - Last 32 bytes: HMAC-SHA256 signature. The HMAC is computed over all preceding bytes (from the magic bytes up to the end of the URL) using the secret key extracted from the audio.

   **Validation Logic & Output**:
   Your script must print exactly one of the following strings to standard output (with a trailing newline) and exit:
   - `FORMAT_ERROR`: If the input is not valid hex, is shorter than 38 bytes, has incorrect magic bytes, or if the specified URL length does not exactly match the remaining bytes before the 32-byte signature.
   - `INVALID_SIG`: If the format is correct but the HMAC-SHA256 signature does not match.
   - `INVALID_URL`: If the signature is valid, but the URL fails the strict security policy. To prevent open redirects and SSRF, the URL MUST start exactly with `https://secure.internal/` and MUST NOT contain the characters `@`, `?`, or any additional `//` beyond the one in the scheme.
   - `ALLOW: <url>`: If all checks pass. (e.g., `ALLOW: https://secure.internal/dashboard`)

You have been provided with a compiled Linux binary of the reference implementation at `/app/oracle_bin`. It has the secret key hardcoded and behaves exactly as your Python script should. You may use it to test your implementation.

Your final submission must be the Python script at `/home/user/redirect_handler.py`. It will be tested via an automated fuzzer comparing its behavior against the reference oracle over thousands of generated inputs.