You are acting as a network security engineer investigating suspicious activity. You have intercepted a suspicious binary and an encrypted file, and captured some HTTP headers and certificates.

Your objective is to write a Bash script at `/home/user/investigate.sh` that automates the forensic analysis of these artifacts. The script must perform the following tasks when executed without arguments:

1. **Binary Analysis:** Extract the SHA-256 hash stored inside a custom ELF section named `.key_hash` from the executable located at `/home/user/intercept_daemon`.
2. **Password Cracking:** Brute-force this SHA-256 hash using the wordlist provided at `/home/user/passwords.txt`. You must implement the brute-force search within your Bash script using standard utilities (e.g., `sha256sum`).
3. **Decryption:** Use the cracked password to decrypt the file `/home/user/traffic_keys.enc`. The file was encrypted using `openssl` with AES-256-CBC and PBKDF2 (`-aes-256-cbc -pbkdf2 -d -pass pass:<PASSWORD>`). The decrypted content will reveal a directory path containing TLS certificates.
4. **Certificate Validation:** In the directory revealed by step 3, there are two certificates: `ca.crt` and `server.crt`. Validate `server.crt` against the root `ca.crt`.
5. **CSP Analysis:** Analyze the intercepted HTTP headers in `/home/user/csp_header.txt`. Extract the exact values/domains allowed by the `script-src` directive in the `Content-Security-Policy` header.
6. **Reporting:** Generate a final JSON report at `/home/user/summary_report.json` containing the results. The JSON must have the following exact structure:
   ```json
   {
     "cracked_password": "<the_plaintext_password>",
     "certificate_valid": <true or false (boolean)>,
     "script_src_values": ["<value1>", "<value2>"]
   }
   ```
   *Note: Ensure the boolean is a JSON boolean, not a string. Extract the script-src values exactly as they appear in the directive, separated by spaces.*

Ensure your script is executable (`chmod +x /home/user/investigate.sh`) and gracefully handles the entire pipeline when run. You may write temporary files to `/tmp` if needed.