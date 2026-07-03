You are a security engineer tasked with rotating credentials for a legacy service after a suspected breach.

In your home directory (`/home/user/`), you will find the following files:
1. `legacy_auth.py`: The source code of the authentication module used by the legacy service.
2. `auth.log`: A recent log file from the service that leaked the hashed token of the `admin` user.
3. `new_secret.txt`: A securely generated 32-character hex string that must be used as the new secret for the admin user.

Your task is to:
1. **Audit the code**: Review `/home/user/legacy_auth.py` and identify the primary CWE (Common Weakness Enumeration) associated with using a weak cryptographic hash function (MD5) for token generation.
2. **Crack the compromised token**: Extract the leaked MD5 token hash for the `admin` user from `/home/user/auth.log`. Write a script to brute-force the 4-digit PIN used to generate this hash based on the logic in `legacy_auth.py`.
3. **Generate a new token**: Generate a new, secure token for the `admin` user. The new token must be computed as the lower-case `SHA-256` hex digest of the string `<username>:<new_secret>`, using the secret found in `/home/user/new_secret.txt`.

Once you have completed these steps, create a report at `/home/user/rotation_report.txt` with exactly three lines in the following format:
Line 1: The CWE ID for the weak hash function vulnerability (Format: `CWE-XXX`)
Line 2: The cracked 4-digit PIN (Format: `XXXX`)
Line 3: The new SHA-256 token hex digest

Do not include any extra text, spaces, or blank lines in the report.