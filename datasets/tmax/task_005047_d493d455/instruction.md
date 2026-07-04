You are an incident responder investigating a recent data breach on a compromised server. You have been provided with an archive of artifacts found in the `/home/user/investigation/` directory. Your goal is to recover the attacker's encrypted communications and redact sensitive user data from the compromised logs before submitting them to the legal team.

Here is what you have in `/home/user/investigation/`:
1. `encrypted_key.pem`: An RSA private key left behind by the attacker, but it is encrypted with a passphrase.
2. `dict.txt`: A dictionary file containing a list of common, weak passwords discovered in the attacker's toolkit.
3. `secret.enc`: A file encrypted using the public key corresponding to `encrypted_key.pem`.
4. `incident_logs.txt`: A raw log file that contains details of the breach, but unfortunately also contains plain-text credit card numbers of customers.

Perform the following tasks:

**Phase 1: Cryptographic Recovery & Brute-Force**
Write a script to brute-force the passphrase of `encrypted_key.pem` using the words in `dict.txt`. 
Once you have successfully cracked the passphrase:
1. Save the exact plaintext passphrase to `/home/user/investigation/passphrase.txt`.
2. Use the decrypted private key to decrypt `secret.enc`. Save the decrypted message to `/home/user/investigation/secret.txt`.

**Phase 2: Sensitive Data Redaction**
The `incident_logs.txt` file contains credit card numbers. You need to identify and redact them based on these algorithmic rules:
- A credit card number in these logs is strictly either 16 consecutive digits (e.g., `1234567812345678`) or 16 digits separated by hyphens in groups of four (e.g., `1234-5678-1234-5678`).
- You must replace the *entire* credit card number string with the exact literal string `[REDACTED]`.
- Do not alter any other text, timestamps, or log formatting.
- Save the newly redacted log file to `/home/user/investigation/clean_logs.txt`.

Ensure your final output files exactly match the requested filenames and formats. Your script(s) can be written in any language of your choice (Bash, Python, etc.) but must complete the task fully within the environment.