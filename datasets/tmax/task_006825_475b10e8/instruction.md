You are a security engineer tasked with rotating credentials for a legacy backup system. You have been provided with an old audit log and an encrypted certificate store, but the password for the store has been lost.

Your tasks are:

1. **Log Parsing:** Parse the log file at `/home/user/auth_audit.log` to find the SHA-256 password hash for the user `sys_backup`. The log contains various authentication events.

2. **Password Cracking (C++):** You know the company's legacy password policy for this system required passwords to be exactly a 4-digit number (from `0000` to `9999`) followed by the suffix `_backup` (e.g., `0000_backup`, `4592_backup`, `9999_backup`).
Write a C++ program at `/home/user/crack.cpp` that brute-forces this specific SHA-256 hash. Compile it (link against OpenSSL, e.g., `-lcrypto`) and run it to recover the plaintext password.
Save the recovered plaintext password to `/home/user/cracked.txt`.

3. **Certificate Management:** The recovered password is the passphrase for the legacy PKCS#12 certificate store located at `/home/user/legacy_store.p12`.
Extract the private key and certificate from this store.
Then, repackage them into a **new** PKCS#12 file at `/home/user/new_store.p12` using the new rotation passphrase: `RotatedSecure123!`.

4. **Access Control:** Ensure the newly created `/home/user/new_store.p12` has strict file permissions of `600`.

Requirements:
- Your C++ program must use OpenSSL (`<openssl/sha.h>`) for the SHA-256 hashing.
- Do not change the underlying certificate or private key, only the PKCS#12 container and its password.