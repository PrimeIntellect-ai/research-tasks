You are a DevSecOps engineer investigating a suspicious policy enforcement mechanism. You have discovered an encrypted policy payload file at `/home/user/payload.txt` (which contains base64-encoded data) and a suspicious TLS certificate at `/home/user/policy.crt`.

Through your initial reverse engineering of the policy agent, you've determined that:
1. The payload is encrypted using a simple XOR cipher.
2. The XOR key used to encrypt the payload is exactly the Common Name (CN) of the Subject in the `/home/user/policy.crt` certificate.
3. The encrypted bytes were then base64 encoded.

Your task is to:
1. Extract the Common Name (CN) from the TLS certificate. You may use standard CLI tools (like `openssl`) for this.
2. Write a Rust program at `/home/user/decoder.rs` that reads the base64 payload from `/home/user/payload.txt`, decodes the base64, and XOR-decrypts it using the extracted Common Name as the repeating key.
3. Compile and run your Rust program.
4. Save the final, decrypted plaintext string to exactly `/home/user/decrypted_policy.txt`.

Ensure your Rust program handles the XOR wrapping correctly (if the payload is longer than the key, the key repeats from the beginning). Do not leave any trailing newlines in the decrypted policy file unless they were part of the original plaintext.