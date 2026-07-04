You are a compliance analyst responsible for generating audit trails for a legacy web application. The application uses a proprietary token format for authentication, and we need to audit the raw contents of these tokens.

You have been provided with an old authorization binary located at `/home/user/legacy_auth`. This is an ELF executable.

Your task is to:
1. Reverse engineer or analyze `/home/user/legacy_auth` to extract the hardcoded 8-byte XOR key used for token encryption. The key is stored in the read-only data section and is prefixed with the string `XOR_KEY=`.
2. Write a Go program at `/home/user/audit.go` that reads a list of tokens from `/home/user/tokens.txt`. Each token in the file is on a new line.
3. For each token, your Go program must:
   a. Base64-decode the token.
   b. Decrypt the decoded payload using a repeating XOR with the 8-byte key you extracted from the binary.
   c. Calculate the SHA-256 hash of the decrypted payload.
   d. Format the decrypted payload as a hexadecimal string.
4. Your Go program must write the results to `/home/user/audit_trail.log` with one line per token in the exact following format:
`Original: <base64_token> | DecryptedHex: <hex_of_decrypted_payload> | SHA256: <sha256_hex_of_decrypted_payload>`

Compile and run your Go program so that `/home/user/audit_trail.log` is generated successfully.