You are a security engineer tasked with rotating credentials and cleaning up sensitive data exposed in legacy application logs. 

An incident occurred where an old private key passphrase and some user credentials were leaked. You must recover the old passphrase, decrypt the legacy logs, redact the sensitive information, and prepare a new key.

Follow these steps:
1. **Passphrase Recovery:** A previous admin left a screenshot of the legacy passphrase in an image file at `/app/legacy_passphrase.png`. Use OCR tools (like `tesseract`, which is installed) to extract the passphrase from this image.
2. **Log Decryption:** Use the extracted passphrase to decrypt the log archive located at `/app/encrypted_logs.tar.enc`. The archive was encrypted using `openssl enc -aes-256-cbc -pbkdf2`. Once decrypted, extract the `server.log` file.
3. **Log Redaction (Python):** Write a Python script at `/home/user/redact.py` to parse `server.log`. The logs contain lines with leaked authentication parameters. You must redact the values of any `password`, `secret_key`, or `session_token` parameters found in the URL query strings or JSON payloads within the logs, replacing the exact leaked value with the string `[REDACTED]`. Save the output to `/home/user/clean.log`.
4. **Certificate Management:** Generate a new RSA 2048-bit private key at `/home/user/new_key.pem` without a passphrase. 

The success of your log redaction will be evaluated using a string-similarity metric against our ground-truth redacted file. You need a similarity score of at least 0.98.