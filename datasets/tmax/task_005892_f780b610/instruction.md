You are assisting a security engineer in rotating credentials for a legacy data processing pipeline. The pipeline expects an obfuscated SSH public key to authorize service accounts, along with a cryptographic hash to verify integrity.

Perform the following steps exactly as specified:

1. Create a directory at `/home/user/credentials`.
2. Generate an ed25519 SSH keypair with no passphrase inside this directory. Name the private key file `service_key` (this will also create the public key `service_key.pub`).
3. The legacy system uses a custom payload encoder. Write a C program at `/home/user/credentials/encoder.c` that reads raw bytes from standard input until EOF. It must XOR each byte with the hexadecimal value `0x5C` and output the result continuously as an uppercase 2-digit hexadecimal string (e.g., if the input is "A", 'A' is 0x41, XOR 0x5C is 0x1D, so output "1D").
4. Compile `encoder.c` to an executable named `encoder` in the same directory using standard `gcc`.
5. Feed the exact contents of `service_key.pub` (including any trailing newlines) into the `encoder` executable via standard input. Save the resulting hex string to `/home/user/credentials/obfuscated_payload.txt`.
6. Compute the SHA-256 hash of `/home/user/credentials/obfuscated_payload.txt`. Extract *only* the 64-character lowercase hex hash (no filenames, no asterisks, no extra whitespace) and save it to `/home/user/credentials/payload_checksum.txt`.

Ensure your C program only relies on standard C libraries (`stdio.h`, etc.). Your environment has standard Linux utilities available.