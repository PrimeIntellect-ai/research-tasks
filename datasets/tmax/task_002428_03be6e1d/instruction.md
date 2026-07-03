You are a security engineer tasked with rotating credentials and securing a legacy data processing pipeline. The previous pipeline passed secrets insecurely via command-line arguments (which leaked them to `/proc/[pid]/cmdline`). You must implement a secure replacement using Go.

Here is your objective:

1. **Setup Secure Storage:**
   - Create a directory at `/home/user/.secrets`.
   - Generate a new, random 32-byte AES key. Base64 encode it and save it to `/home/user/.secrets/new_aes.key`. Ensure this file has `0600` permissions.
   - Generate a new SSH ed25519 keypair in `/home/user/.ssh/new_service_key` protected by the passphrase `rotated_pass_2024`. Ensure the private key has `0600` permissions.

2. **Process Legacy Data:**
   - Write a Go program at `/home/user/rotate.go`.
   - The program must decrypt the legacy data located at `/home/user/data/legacy.enc`.
   - The legacy data is a hex-encoded string containing an AES-GCM encrypted payload. The first 12 bytes of the decoded binary data constitute the nonce, followed by the ciphertext.
   - The old insecure key used for encryption is the 32-byte string: `32-byte-old-insecure-key-1234567`

3. **Pattern Extraction & Re-encryption:**
   - The decrypted legacy payload contains system logs. Using Go's regex capabilities, extract all valid IPv4 addresses from this plaintext.
   - Join the unique extracted IP addresses into a comma-separated string (e.g., `192.168.1.1,10.0.0.1`).
   - Read your newly generated key from `/home/user/.secrets/new_aes.key` (remember to base64 decode it).
   - Encrypt the comma-separated IP string using AES-GCM with your new key. Generate a random 12-byte nonce, prepend it to the ciphertext, and save the entire result as a hex-encoded string to `/home/user/data/ips_secured.enc`.

4. **Execution:**
   - Write a shell script at `/home/user/run.sh` that compiles and runs your Go program. Ensure no secrets are passed as command-line arguments in this script.

Run your script so that `/home/user/data/ips_secured.enc` and all the new keys are successfully generated.