You are a security engineer tasked with rotating credentials for a legacy internal service. The service has a few security issues that need to be addressed as part of the rotation process. 

Your objectives are:

1. **Reverse Engineering:** We lost the old credential encryption key. However, we know it is hardcoded inside a legacy compiled binary located at `/home/user/legacy_key_service`. Analyze this binary to extract the old key. The key is a 16-character string starting with `OLD_`.

2. **Decryption:** A file containing the current encrypted credentials is located at `/home/user/data/creds.enc`. The file is base64 encoded. Once decoded, the bytes were encrypted using a simple repeating-key XOR cipher with the old key you extracted. Decrypt the contents of this file. Write the plaintext credentials to `/home/user/rotation.log`.

3. **Vulnerability Analysis & Secure Coding:** The source code for the credential retrieval service is located at `/home/user/cred_server.rs`. It contains a severe Command Injection vulnerability in how it searches for user credentials. 
Write a fixed version of this Rust code to `/home/user/cred_server_fixed.rs`. The fixed version must completely avoid using shell commands (e.g., no `std::process::Command` executing `sh`, `bash`, `grep`, etc.) and instead read the file using Rust's standard filesystem and string manipulation libraries (`std::fs::read_to_string`, `.lines()`, `.contains()`, etc.).

4. **Encryption & Access Control:** Re-encrypt the plaintext credentials you obtained in Step 2 using the new key: `NEW_KEY_99887766`. Use the same base64-encoded XOR cipher method. Save the new encrypted credentials to `/home/user/data/creds_v2.enc`. Finally, ensure that the new file has strictly restricted file permissions: only the owner should have read access (i.e., `0400`), with no access for group or others.

Requirements:
- You must use Rust to compile or run any scripts you write, though standard shell utilities (like `strings`, `chmod`, etc.) are fully permitted.
- Provide the exact decrypted contents in `/home/user/rotation.log`.
- Ensure `/home/user/data/creds_v2.enc` exists with the exact permissions `0400`.