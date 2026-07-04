You are an algorithmic penetration tester evaluating a simulated web environment. You have intercepted several artifacts from a vulnerable server, including HTTP logs, hashed credentials, and server certificates.

Your objective is to write a Rust program that analyzes these artifacts, chains the findings together, and produces a final JSON report.

**Artifacts provided to you:**
1. `/home/user/traffic.log`: A text file containing raw HTTP request and response headers separated by blank lines.
2. `/home/user/hashes.txt`: A text file containing SHA256 hashes (one per line). These are known to be hashed 4-digit numeric PINs (from `0000` to `9999`) combined with a specific salt.
3. `/home/user/cert.pem`: An X.509 certificate in PEM format.

**Your Rust program must perform the following tasks:**

1. **HTTP Header & Cookie Inspection (and CSP Analysis):**
   Parse `/home/user/traffic.log`. Find the *first* HTTP response block that contains a `Content-Security-Policy` header which includes the unsafe directive `'unsafe-inline'`. From the corresponding HTTP *request* block immediately preceding this response, extract the value of the `Session-Id` cookie.

2. **Certificate Parsing:**
   Read `/home/user/cert.pem`. Extract the Common Name (CN) from the Subject field of the certificate. You may use standard string manipulation or shell commands via Rust, or a crate of your choice, to parse the PEM text and find the `CN=...` value.

3. **Password Cracking:**
   The hashes in `/home/user/hashes.txt` were generated using `SHA256(PIN + SALT)`, where `+` is string concatenation. The `SALT` is the exact Common Name (CN) extracted in Step 2.
   Write a brute-force search in your Rust program to find the original 4-digit PIN for each hash.

4. **Reporting:**
   Your Rust program must output a JSON file at `/home/user/report.json` with the following exact schema:
   ```json
   {
     "vulnerable_session_id": "extracted_session_id_here",
     "certificate_cn": "extracted_cn_here",
     "cracked_pins": [
       "0123",
       "4567"
     ]
   }
   ```
   *Note: The `cracked_pins` array should contain the PINs in the same order as their corresponding hashes in the `hashes.txt` file.*

**Constraints & Setup:**
* Create your Rust project in `/home/user/analyzer`.
* You may use any necessary crates (e.g., `sha2`, `hex`, `serde_json`).
* Ensure your Rust program compiles and runs successfully to produce the `/home/user/report.json` file.