You are an incident responder investigating a compromised system. You have found a suspicious Rust-based authentication binary at `/home/user/vuln_auth` and an encrypted data file at `/home/user/secret.enc`. 

Initial analysis suggests that the binary uses JSON Web Tokens (JWT) for authentication but contains a critical vulnerability: it accepts tokens where the algorithm is set to "none" (the classic `alg=none` bypass). 

To prove this vulnerability and recover the encrypted data, you must:
1. **Analyze the Binary**: Inspect `/home/user/vuln_auth` to find the required service identifier. The binary expects the JWT payload to contain a specific `service_id` string that matches the regular expression `SVC_[a-f0-9]{8}`. It is hardcoded in the binary's read-only data section.
2. **Craft the Exploit**: Write a Rust program at `/home/user/craft_token.rs` that generates a malicious JWT. 
   - The JWT Header must be exactly: `{"alg":"none","typ":"JWT"}`
   - The JWT Payload must be exactly: `{"role":"admin","service_id":"<FOUND_SERVICE_ID>"}`
   - The JWT must be correctly formatted as `Base64Url(Header).Base64Url(Payload).` (Note the trailing dot indicating an empty signature, and ensure Base64Url encoding does NOT include padding like `=`).
3. **Execute the Bypass**: Run the binary with your crafted token as the first argument: `/home/user/vuln_auth <CRAFTED_TOKEN>`. 

If successful, the binary will decrypt `/home/user/secret.enc` and write the plain text to `/home/user/flag.txt`. 

Your final goal is to successfully produce the `/home/user/flag.txt` file. Leave the Rust source code of your exploit at `/home/user/craft_token.rs`.