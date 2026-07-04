You are a security engineer tasked with rotating credentials for a legacy authentication daemon. The current implementation has a critical security flaw: it accepts credentials via command-line arguments, which leaks the plaintext passwords to any local user monitoring `/proc`.

Your objective is to validate a newly issued encrypted credential, securely decrypt it, and patch the legacy C daemon to ingest the credential without leaking it to process monitoring tools.

Perform the following steps:

1. **Validate the Certificate Chain:**
   In the directory `/home/user/certs/`, you will find three certificates: `root_ca.pem`, `sub_ca.pem`, and `service.pem`. Validate that `service.pem` is correctly signed by the chain up to `root_ca.pem`. Save the standard output of your `openssl verify` command to `/home/user/cert_verify.log`.

2. **Verify the Credential Signature:**
   You have been provided an encrypted credential payload at `/home/user/new_cred.enc` and its signature at `/home/user/new_cred.sig`. The signature was generated using SHA-256 and the private key corresponding to `service.pem`. Verify the signature against `new_cred.enc` using the public key extracted from `service.pem`.

3. **Decrypt the Credential:**
   Once the signature is verified, decrypt `/home/user/new_cred.enc`. It was encrypted using `aes-256-cbc` with `pbkdf2`. The decryption passphrase is saved in plaintext inside `/home/user/decryption_key.pass`. 

4. **Patch the Legacy Source Code:**
   The source code for the authentication daemon is located at `/home/user/legacy_auth.c`. Currently, it reads the password from `argv[1]`. Modify the C code to read a single line (up to 64 characters) from standard input (`stdin`) instead of relying on command-line arguments. Ensure you strip any trailing newline characters (`\n` or `\r`) from the read string. 

5. **Compile and Run:**
   Compile your modified code to an executable named `/home/user/safe_auth` using `gcc`. Finally, execute `/home/user/safe_auth` and pipe your decrypted credential into it via `stdin`. If successful, the program will automatically generate a file named `/home/user/rotation_success.log`.