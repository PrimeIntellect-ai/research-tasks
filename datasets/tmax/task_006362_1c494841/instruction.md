You are a network security engineer investigating a potentially compromised server. You suspect that a legacy monitoring daemon is leaking authentication credentials via its command-line arguments, which are visible in the process tree. 

We have captured a snapshot of the `/proc` directory for suspicious processes and stored them in `/home/user/proc_dumps/`. 

Your objective is to extract the leaked credential, crack it, and use it to restore access to a locked TLS certificate key.

Follow these specific steps:

1. **Analyze the Process Dumps:** Inspect the `cmdline` files within the subdirectories of `/home/user/proc_dumps/`. Look for a process that was launched with the `--auth-token` argument. The value associated with this argument is a base64-encoded payload.
2. **Decode the Payload:** The decoded payload follows the format `username:md5_hash`. Extract the MD5 hash.
3. **Write a Password Cracker in C:** 
   Write a C program at `/home/user/cracker.c` that brute-forces the extracted MD5 hash. You know that the original password is exactly a 4-digit PIN (e.g., `0000` to `9999`). 
   Your C program should accept the MD5 hash as a command-line argument, find the matching 4-digit PIN, and print ONLY the PIN to standard output. Compile it to `/home/user/cracker`. (You may use OpenSSL's `libcrypto` via `-lcrypto` for MD5 functions).
4. **Unlock the Private Key:** 
   There is an encrypted RSA private key located at `/home/user/encrypted.key`. The passphrase for this key is the 4-digit PIN you just cracked.
5. **Generate a CSR:**
   Using the decrypted key, generate a new Certificate Signing Request (CSR) and save it to `/home/user/server.csr`. 
   The CSR must have the following exact Subject details:
   - Country (C): `US`
   - Organization (O): `SecCorp`
   - Common Name (CN): `internal.seccorp.local`

Ensure that the final CSR file is located exactly at `/home/user/server.csr`.