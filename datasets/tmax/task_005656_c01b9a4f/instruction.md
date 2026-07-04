You are a security engineer tasked with rotating database credentials in a Linux environment. 

You need to securely decrypt an old credential, generate a new one, encrypt it using a validated certificate's public key, and then securely trigger a deployment script using process environment isolation.

Here are the specific steps you must complete:

1. **Certificate Chain Validation**:
   In `/home/user/certs/`, there are three certificates: `rootCA.pem`, `intermediate.pem`, and `db_service.pem`. 
   Verify that `db_service.pem` is valid against the provided certificate chain (`rootCA.pem` and `intermediate.pem`). 
   If valid, extract the RSA public key from `db_service.pem` and save it to `/home/user/rotation/pubkey.pem`.

2. **Decryption and Rotation**:
   In `/home/user/secrets/`, there is an encrypted file named `legacy_secret.enc`. This file was encrypted using `openssl enc` with the `aes-256-cbc` cipher, the `-pbkdf2` flag, and the password `admin123`.
   Decrypt this file to reveal the old database password.
   Create a new password by taking the exact old password and appending the string `-ROTATED` to it.

3. **Encryption and Integrity**:
   Encrypt the new password using the RSA public key you extracted (`/home/user/rotation/pubkey.pem`) with `openssl pkeyutl`. 
   Save the encrypted new password to `/home/user/rotation/new_secret.enc`.
   Calculate the SHA256 checksum of `/home/user/rotation/new_secret.enc` and save the standard `sha256sum` output to `/home/user/rotation/checksum.txt`.

4. **Process Isolation Deployment**:
   There is a deployment script located at `/home/user/deploy.sh`. 
   You must execute this script in a strictly isolated, empty environment (stripping all standard environment variables like `$USER`, `$HOME`, `$PATH`, etc.) to prevent environment-based injection attacks.
   The ONLY environment variable that must be passed to the script is `DEPLOY_HASH`, which should contain the raw 64-character SHA256 hash you calculated in step 3.

Ensure all outputs are placed exactly in the `/home/user/rotation/` directory as specified.