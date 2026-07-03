You are a forensics analyst investigating a compromised Linux host. The attacker left behind a ransomware note as an image and a backdoored HTTP service that receives commands. We need you to reverse-engineer their command-decryption pipeline so we can decrypt intercepted traffic.

You have access to the attacker's ransom note image at `/app/evidence/ransom_note.png`. 

Your objective is to write a standalone executable script at `/home/user/payload_decoder` that behaves exactly like the attacker's command receiver. The script must read a raw HTTP POST request from standard input (`stdin`) and output the decrypted command or an error message to standard output (`stdout`).

Here is the specification for `/home/user/payload_decoder`:

1. **HTTP Parsing**: Read the full HTTP POST request from `stdin`. You must extract:
   - The `Session-ID` cookie from the `Cookie` header.
   - The `X-Ransom-Token` HTTP header.
   - The HTTP POST body (which contains a hex-encoded encrypted payload).

2. **Error Handling (Malformed)**: If the `Session-ID` cookie, `X-Ransom-Token` header, or POST body is missing, immediately print exactly `MALFORMED_REQUEST` to stdout and exit.

3. **Key and Salt Extraction**: The attacker's image (`/app/evidence/ransom_note.png`) contains two crucial pieces of text: a `MASTER_KEY` (a 32-character hex string representing a 16-byte AES key) and a `SALT` string. You will need to extract these (e.g., using OCR tools like `tesseract` which are available on the system) and use them in your script.

4. **Token Validation**: The attacker uses a custom validation scheme. To authorize the command, the `X-Ransom-Token` header must exactly equal the MD5 hash (in lowercase hex) of the concatenated string: `<Session-ID><SALT>`.
   - If the token does not match, print exactly `INVALID_TOKEN` to stdout and exit.

5. **Decryption**:
   - The encryption algorithm is AES-128-CBC.
   - The Encryption Key is the 16-byte raw binary form of the `MASTER_KEY` found in the image.
   - The Initialization Vector (IV) is the 16-byte raw MD5 hash of the `Session-ID` string.
   - The POST body is the hex-encoded ciphertext. Decode the hex, decrypt it using AES-128-CBC, and output the decrypted plaintext string to stdout (without a trailing newline unless it's part of the decrypted payload). Assume PKCS#7 padding.

Ensure your script is executable (`chmod +x /home/user/payload_decoder`). You may write this in any language available on the system (Python, bash+openssl, Perl, etc.), as long as the entry point `/home/user/payload_decoder` can be executed directly.

We will verify your solution by fuzzing your `/home/user/payload_decoder` against our reference implementation using thousands of randomly generated HTTP requests to ensure bit-exact output matches.