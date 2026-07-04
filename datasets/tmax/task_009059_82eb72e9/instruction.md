You are a compliance analyst investigating a series of suspected open redirect attacks on a web server's login flow. You have been provided with a web server access log at `/home/user/access.log`.

The login endpoint accepts a `token` parameter which contains an encrypted string representing the redirect destination after authentication (e.g., `GET /login?token=...`).

The development team used a weak custom encryption scheme for these tokens:
1. The plaintext redirect URL is XOR-encrypted using a repeating key.
2. The XOR key is the string `"COMPLIANCE"`.
3. The resulting bytes are Base64 encoded.

Your task is to generate an audit trail of all successful open redirect exploits found in the log:
1. Parse `/home/user/access.log` and extract all `token` parameters.
2. Decrypt each token back to its plaintext string.
3. Identify which decrypted tokens are open redirect attempts. An open redirect attempt is defined as any decrypted token that begins with exactly `http://` or `https://` (relative paths like `/dashboard` or `/settings` are legitimate and should be ignored).
4. Write the decrypted open redirect URLs to `/home/user/redirects.txt`, one per line, in the exact order they appear in the log.
5. Compute the SHA-256 hash of `/home/user/redirects.txt` and output the hexadecimal digest to `/home/user/audit_checksum.txt`.

Ensure your output files match these exact paths and formats.