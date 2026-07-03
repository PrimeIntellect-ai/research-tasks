You are performing an internal penetration test and have discovered an encrypted file containing a critical SSH private key at `/home/user/encrypted_ssh_key.enc`. 

Through prior reconnaissance, you know the following:
1. A hidden service is running on `localhost` on a port between `8000` and `8020`.
2. This service is protected by TLS. 
3. The passphrase used to encrypt the SSH private key is exactly the **serial number of the TLS certificate** presented by this hidden service, represented as a base-10 integer string (e.g., `123456789`).
4. The SSH key was encrypted using standard OpenSSL AES-256-CBC with PBKDF2 (`openssl enc -aes-256-cbc -pbkdf2`).

Your objective:
1. Write a Python script to scan ports `8000` through `8020` on `localhost` to identify the active TLS service.
2. Extract the TLS certificate from the responsive port and determine its serial number.
3. Decrypt `/home/user/encrypted_ssh_key.enc` using the extracted serial number as the passphrase. Save the decrypted private key to `/home/user/id_rsa`.
4. Calculate the SHA256 fingerprint of the decrypted SSH private key using standard SSH utilities.
5. Save ONLY the SHA256 fingerprint string (e.g., `SHA256:abcdefg1234567...`) into a file named `/home/user/result.txt`. Do not include the key size or comment in `result.txt`, just the `SHA256:...` portion.

Ensure the final decrypted key `/home/user/id_rsa` has the appropriate restrictive file permissions, or SSH utilities may refuse to process it.