You are a forensics analyst responding to a compromised Linux host. The attacker installed a persistent backdoor, modified system permissions to maintain privilege escalation vectors, and left traces in the web server logs. Your objective is to recover evidence, identify the privilege escalation vector, and forge an authentication token to extract the final payload using the attacker's own cryptography.

Please complete the following steps:

1. **Privilege Escalation Auditing:** 
   The attacker placed several utilities in `/home/user/bin/`. One of these binaries was maliciously modified to have the SUID (Set Owner User ID) bit set, allowing it to execute with owner privileges. Identify the absolute path of this specific binary and write it to `/home/user/evidence/suid_bin.txt`.

2. **Security Log Parsing and Correlation:**
   Analyze the web server logs located at `/home/user/evidence/server.log`. The attacker successfully accessed a hidden endpoint at exactly the path `/hidden/payload` and received an HTTP 200 OK response. Identify the IP address of the attacker from this successful request. Write the IP address to `/home/user/evidence/attacker_ip.txt`.

3. **Token Generation and Validation (Rust):**
   The attacker left behind a partial source code snippet of their token generation logic in `/home/user/attacker_tools/crypto_spec.txt`. The token is constructed as a plaintext string `IP:<attacker_ip>:EXP:<expiration_timestamp>` followed by a `.` (dot), and then the lower-case hex-encoded HMAC-SHA256 signature of that plaintext string.
   
   The secret key used for the HMAC is `F0r3ns1csK3y!`.
   
   Create a new Rust project in `/home/user/token_forge`. Write a Rust program that uses the `hmac` and `sha2` crates (you will need to add these to your `Cargo.toml`) to generate a valid token. 
   
   Use the attacker's IP address you discovered in step 2.
   Set the expiration timestamp strictly to `1900000000`.
   
   Your Rust program must output the final token string to `/home/user/evidence/forged_token.txt`.
   
   The format of the final token in the file must be exactly:
   `IP:<attacker_ip>:EXP:1900000000.<hex_encoded_hmac_sha256>`

Ensure all output files are placed in the `/home/user/evidence/` directory as requested.