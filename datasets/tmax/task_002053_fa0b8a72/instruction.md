You are a compliance analyst tasked with generating an audit trail for a legacy application, while also assessing its security posture. An undocumented, legacy audit logging service binary is located at `/home/user/audit_server` and is actively running on port `8080`. 

You must perform a multi-phase analysis, reverse engineering, decryption, and vulnerability scanning process to bring this service into compliance. You may use any programming language for the scripts you write.

Complete the following objectives:

1. **Reverse Engineering:** 
   Analyze the compiled binary `/home/user/audit_server`. Identify the hardcoded encryption key used by the service to secure logs. Furthermore, analyze the binary to discover a hidden, undocumented administrative HTTP endpoint (which represents a vulnerability).

2. **Decryption:**
   You have been provided an intercepted encrypted log file at `/home/user/legacy_logs.enc`. The binary encrypts logs using a simple repeating-key XOR cipher (using the hardcoded key you found), followed by standard Base64 encoding. Write a script to decrypt this file and output the plaintext to `/home/user/decrypted_logs.txt`.

3. **Automated Vulnerability Scanning:**
   Write an automated scanning script that sends a GET request to the hidden, vulnerable endpoint you discovered on `http://127.0.0.1:8080`. Save the exact HTTP response body returned by this hidden endpoint to `/home/user/vulnerability_proof.txt`.

4. **Compliance Reporting:**
   Generate a final audit trail report at `/home/user/compliance_report.json` in strict JSON format. It must contain exactly the following keys:
   - `"encryption_key"`: (String) The exact hardcoded key found in the binary.
   - `"hidden_endpoint"`: (String) The exact URL path of the hidden endpoint (must start with `/`).
   - `"decrypted_lines"`: (Integer) The total number of lines in your `/home/user/decrypted_logs.txt` file.

Ensure all output files are placed exactly at the specified absolute paths. You have full freedom to install necessary tools (like `nmap`, `strings`, `radare2`, etc.) and write helper scripts in your preferred language to achieve this.