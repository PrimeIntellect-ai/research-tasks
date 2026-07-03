You are acting as a penetration tester analyzing a web server's logs. We suspect the server has an open redirect vulnerability in its login flow that is actively leaking encrypted authentication tokens to malicious third-party domains.

You need to analyze the logs, extract the leaked tokens, decrypt them, validate them, and generate a secure report of the compromised users.

Here is the information you have:
- The server access log is located at `/home/user/pentest_data/access.log`.
- The legitimate domain for the application is `app.local`. Any redirect to a host other than `app.local` (e.g., `evil.com`, `attacker.net`) is considered a malicious open redirect.
- The vulnerability manifests in the `/login` endpoint. Malicious requests look like this:
  `GET /login?redirect=http://[malicious_domain]/somepath?token=[ENCRYPTED_TOKEN] HTTP/1.1`
- The `token` parameter contains the leaked authentication token, which is Base64 encoded and encrypted.
- The encryption algorithm used is AES-256-CBC with PBKDF2. The password to decrypt these tokens was found during an earlier phase of the pentest and is stored in `/home/user/pentest_data/key.txt`. (You can decrypt a token using: `openssl enc -d -aes-256-cbc -pbkdf2 -pass file:/home/user/pentest_data/key.txt -a`).
- Once decrypted, the token payload has the format: `username:expiration_epoch` (e.g., `jsmith:1735689600`).
- A token is only considered valid and compromised if its `expiration_epoch` is strictly greater than `1735689600` (which corresponds to Jan 1, 2025).

Your task is to write a bash script or use command-line tools to do the following:
1. Parse `/home/user/pentest_data/access.log` to identify all malicious open redirects that leak a token. (Ignore redirects to `app.local`).
2. Extract the encrypted token from the URL.
3. Decrypt the token to get the payload.
4. Validate the token by ensuring the expiration epoch is > 1735689600.
5. Extract the `username` from valid tokens.
6. Write the compromised usernames to `/home/user/compromised_users.txt`. Each username must be on a new line. The list must be sorted alphabetically in ascending order, with no duplicates.
7. To protect this sensitive finding, you must set the file permissions of `/home/user/compromised_users.txt` to strictly `600` (read and write for the owner only).

Ensure the final file `/home/user/compromised_users.txt` is created with the correct content and permissions.