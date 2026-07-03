You are a security engineer tasked with rotating credentials for a legacy service. The service currently uses weak passwords stored as SHA-256 hashes, and we need to migrate these users to secure API tokens.

Your task is to write a Rust tool that cracks the legacy passwords, generates new secure tokens, and outputs a migration mapping file. 

Here are the details of the environment and what you must do:

1. **Password Cracking**:
   - You have a legacy database export at `/home/user/legacy_db.csv`. It contains comma-separated values in the format: `username,sha256_hex_hash`.
   - You have a dictionary of common passwords at `/home/user/wordlist.txt`.
   - Write a Rust application in `/home/user/credential_rotator` (you'll need to initialize the project via Cargo) that reads both files, and brute-forces the SHA-256 hashes to find the plaintext passwords for each user.

2. **Token Generation**:
   - For every user whose password you successfully crack, you must generate a new secure API token.
   - The token must be an HMAC-SHA256 digest of the `username`.
   - The secret key for the HMAC is stored as plain text in `/home/user/master.key`.
   - The resulting token must be formatted as a lowercase hexadecimal string.

3. **Output format**:
   - Your Rust program must output the results to `/home/user/rotated_credentials.csv`.
   - The file must contain one line per successfully cracked user in the exact format: `username,cracked_password,new_token`
   - The lines in the output CSV must be sorted alphabetically by `username`.

You may use standard Rust crates (e.g., `sha2`, `hmac`, `hex`) by adding them to your `Cargo.toml`. You do not need to preserve users whose passwords cannot be found in the wordlist.

Once your Rust program has run and generated `/home/user/rotated_credentials.csv`, the task is considered complete.