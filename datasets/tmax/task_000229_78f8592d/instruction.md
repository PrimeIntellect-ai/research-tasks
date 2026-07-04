You are a network security engineer investigating a potentially compromised system. During an audit, you discovered that an old authentication service (`legacy_auth.sh`) is running in the background and insecurely leaking a sensitive cryptographic key via its command-line arguments. 

You have intercepted a signed authentication token file (`/home/user/token.enc`) and its RSA signature (`/home/user/token.sig`). The token is encrypted using a weak repeating-key XOR cipher, with the leaked key used as the secret. The server's public certificate is available at `/home/user/server.crt`.

Your objective is to verify, decrypt, and validate this token using the terminal.

Perform the following tasks:
1. Extract the public key from the X.509 certificate `/home/user/server.crt`.
2. Use the extracted public key to verify the SHA-256 RSA signature `/home/user/token.sig` against the encrypted token file `/home/user/token.enc`.
3. Locate the running `legacy_auth.sh` process and extract its command-line argument, which is the secret XOR key.
4. Write a pure Bash script named `/home/user/decrypt.sh` that takes the hex-encoded `/home/user/token.enc` and the secret key to perform a repeating-key XOR decryption. The script must output the decrypted plaintext token.
5. Run your script and save the decrypted plaintext token to `/home/user/decrypted_token.txt`.
6. Verify the file integrity of your decrypted token by computing its SHA-256 hash. Ensure the hash matches the value inside `/home/user/expected_hash.txt`.

Ensure your Bash script handles the hex decoding and XOR operations correctly. Do not write the decryption logic in Python, Ruby, or Perl; use Bash.