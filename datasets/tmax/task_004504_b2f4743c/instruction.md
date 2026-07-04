You are a DevSecOps engineer enforcing policy-as-code for a legacy application. The system receives encrypted payload strings in HTTP headers, and we need a reliable Bash script to validate and decrypt these payloads.

An image of the physical security policy document is located at `/app/policy_doc.png`. Use OCR (e.g., `tesseract`) to read it. It contains a line specifying the master key: `POLICY_KEY: <14 characters>**`. The last two characters are obscured by a smudge, but it is known that they are both uppercase English letters (A-Z).

You are also provided with a valid reference payload at `/app/test_payload.hex`. When decrypted with the correct 16-character key, the plaintext is exactly `VALID_DEVSECOPS_TEST` (no newline). You must brute-force the missing two characters to discover the exact AES key.

Once you have discovered the key, create the script `/home/user/verify_payload.sh`. 
The script must take exactly one argument: a hexadecimal string representing the payload.

**Payload Structure (when hex-decoded to raw bytes):**
- **Bytes 0-15 (16 bytes):** Initialization Vector (IV)
- **Bytes 16-47 (32 bytes):** HMAC-SHA256 signature
- **Bytes 48+ (variable length, multiple of 16 bytes):** AES-128-CBC ciphertext

**Script Execution & Validation Rules:**
1. **Format Check:** If the input argument contains non-hexadecimal characters, or if the total decoded raw byte length is less than 64 bytes, the script must print exactly `ERROR: INVALID_FORMAT` to standard output and exit with status `1`.
2. **Integrity Verification:** Calculate the HMAC-SHA256 signature of the concatenated raw bytes of `(IV + Ciphertext)` using the discovered 16-character secret key. Compare it to the provided HMAC in the payload. If they do not match, print exactly `ERROR: INTEGRITY_VIOLATION` to standard output and exit with status `2`.
3. **Decryption:** Decrypt the ciphertext using `aes-128-cbc`, the discovered secret key, and the IV. Do not use salt (`-nosalt`). 
4. **Decryption Error Check:** If the decryption command fails (e.g., bad padding), print exactly `ERROR: DECRYPTION_FAILED` to standard output and exit with status `3`.
5. **Success:** If decryption is successful, print the exact decrypted plaintext to standard output (do not append a newline unless one is in the plaintext) and exit with status `0`.

Your script `/home/user/verify_payload.sh` will be rigorously tested against an automated fuzzer. It must be bit-exact equivalent to our reference implementation, handling hundreds of malformed, malicious, and valid inputs perfectly. You may hardcode the discovered key inside your script for efficiency.