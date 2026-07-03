You are a security engineer tasked with rotating credentials and securing a legacy data processing pipeline. 

We have a legacy script that currently leaks a sensitive database password by passing it as a command-line argument, which makes it visible to all users on the system via `/proc` and `ps`. The script also carelessly logs this password. Finally, the script relies on a certificate bundle, but its integrity needs to be verified before proceeding.

Here is the current state of the system in `/home/user/`:
1. `/home/user/legacy_runner.sh`: A shell script that executes the python processor. It currently passes the password `SUPER_SECRET_99!` via the `--db-pass` command-line argument.
2. `/home/user/processor.py`: The python script that parses the arguments, "processes" data, and writes to a log file at `/home/user/processing.log`.
3. `/home/user/cert_bundle.pem`: A certificate file used for the theoretical database connection.
4. `/home/user/cert_hash.sha256`: A file containing the expected SHA-256 checksum of `cert_bundle.pem` (formatted as `hash  filename`).

Your objectives:
1. **File Integrity Verification**: Verify the SHA-256 checksum of `/home/user/cert_bundle.pem` against the hash in `/home/user/cert_hash.sha256`. Create a file named `/home/user/cert_status.txt` and write exactly the word `VERIFIED` into it if the hash matches, or `FAILED` if it does not.
2. **Prevent Process-Level Credential Leaks**: Modify `/home/user/legacy_runner.sh` and `/home/user/processor.py` so that the database password is NO LONGER passed as a command-line argument. Instead, `legacy_runner.sh` must pass the password to the Python script using an environment variable named `DB_PASSWORD`.
3. **Sensitive Data Redaction**: Update `/home/user/processor.py` so that when it writes its output to `/home/user/processing.log`, the actual password is redacted and replaced with the exact string `[REDACTED]`.

When you are done, executing `/home/user/legacy_runner.sh` should run the python script successfully, but `ps aux` should not show the password, and `/home/user/processing.log` should not contain the plaintext password.