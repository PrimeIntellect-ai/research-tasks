You are acting as a security engineer responding to a credential leak. An attacker recorded their terminal while exfiltrating data, and we recovered the screen recording.

A video file is located at `/app/leak_capture.mp4`. It shows a scrolling terminal with raw HTTP requests. Some of these requests contain leaked authentication tokens in the HTTP headers (e.g., `Authorization: Bearer <token>` or `Cookie: session=<token>`).

Your task is to perform a complete credential rotation for the compromised accounts using Rust:

1. **Extract Leaked Identifiers:**
   Extract frames from `/app/leak_capture.mp4` and use an OCR tool (like `tesseract-ocr`, which you may need to install) to read the text.
   Identify all leaked tokens. The tokens are Base64-encoded JSON payloads. Decode them to extract the compromised `uid` (User ID) from each token.

2. **Secure the Master Key:**
   The new master secret key for generating tokens is located at `/app/master_secret.key`.
   For security reasons, ensure its file permissions are set to strictly read-only for the owner (`0400`). 

3. **Write a Rust Token Generator:**
   Create a Rust project in `/home/user/rotator`.
   Write a Rust program that reads the extracted compromised `uid`s and generates a new, rotated token for each.
   The program **must** programmatically verify that `/app/master_secret.key` has exactly `0400` permissions before proceeding. If it does not, the program should panic.
   
   The new token format must be:
   `{uid}.{signature}`
   Where `{signature}` is the lowercase hex string of the HMAC-SHA256 hash of the string `{uid}` using the contents of `/app/master_secret.key` as the HMAC key.

4. **Output Generation:**
   Run your Rust program to generate the new tokens.
   Save the results to `/home/user/rotated_credentials.json` in the following format:
   ```json
   {
     "uid1": "uid1.abcdef123456...",
     "uid2": "uid2.9876543210fe..."
   }
   ```

To succeed, you must correctly identify the compromised UIDs from the video and correctly generate the cryptographic tokens using Rust. The evaluation will measure the F1 accuracy of your generated JSON file against the true list of leaked UIDs and their mathematically correct rotated tokens. You must achieve an accuracy of at least 85% to account for potential OCR artifacts.