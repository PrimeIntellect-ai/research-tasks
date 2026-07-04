You are acting as a security engineer responding to an incident. A web server's login flow contained an open redirect vulnerability that inadvertently logged sensitive user credentials (passwords and OAuth tokens) in plaintext into the application's access logs. Furthermore, the database password may have been exposed and needs to be rotated.

You must perform a full credential rotation and log redaction process entirely in the Linux terminal. Write a Bash script at `/home/user/incident_response.sh` that performs the following steps when executed. (You may also run the commands directly or execute your script to produce the final state).

**Step 1: Sensitive Data Redaction**
The application log file is located at `/home/user/app/logs/access.log`. It contains HTTP GET requests where query parameters `password` and `token` are exposed.
* Read `/home/user/app/logs/access.log`.
* Use a stream editor (like `sed`) to replace the values of the `password` and `token` query parameters with the exact string `[REDACTED]`. (e.g., `password=secret&token=123` becomes `password=[REDACTED]&token=[REDACTED]`).
* Save the redacted output to `/home/user/app/logs/access_redacted.log`.

**Step 2: Checksum Generation**
To assure data integrity before archival:
* Calculate the SHA-256 checksum of the newly created `/home/user/app/logs/access_redacted.log`.
* Save the standard output of the `sha256sum` command directly to `/home/user/archive/redacted_hash.txt`.

**Step 3: Encryption for Archival**
The redacted log must be encrypted before being stored.
* Encrypt `/home/user/app/logs/access_redacted.log` using OpenSSL with the `aes-256-cbc` cipher and the `-pbkdf2` key derivation function.
* Use the symmetric key stored in `/home/user/keys/backup.key` (pass it using `-pass file:/home/user/keys/backup.key`).
* Output the encrypted file to `/home/user/archive/access_redacted.log.enc`.
* Ensure you delete the plaintext `/home/user/app/logs/access_redacted.log` after encryption.

**Step 4: Credential Rotation**
The database configuration is located at `/home/user/app/config.env`. It contains a line starting with `DB_PASSWORD=`.
* The new plaintext password you must use is `SuperSecurePwd2024!`.
* Instead of saving the plaintext password in the config, you must calculate its SHA-256 hash (do not include a trailing newline when hashing the string).
* Update `/home/user/app/config.env` so that the `DB_PASSWORD` value is replaced with the new SHA-256 hash. (e.g., `DB_PASSWORD=<new_hash_value>`).

Ensure your final state reflects all these changes. Your script `/home/user/incident_response.sh` should be executable and run without errors.