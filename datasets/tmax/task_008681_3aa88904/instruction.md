You are a security engineer tasked with rotating credentials and securing an internal certificate management tool.

An internal C++ utility, `/home/user/rotate_cli.cpp`, is used to deploy new TLS certificates to a target directory. However, a preliminary security scan flagged the code for potential vulnerabilities. 

Your task consists of four phases:

**Phase 1: Code Auditing & CWE Identification**
1. Review the source code of `/home/user/rotate_cli.cpp`.
2. Identify the two major security vulnerabilities in the code:
   - One vulnerability allows arbitrary OS command execution via improper input handling.
   - One vulnerability allows Cross-Site Scripting (XSS) when generating the HTML status report.
3. Determine the official MITRE CWE IDs for these two vulnerabilities.
4. Create a file named `/home/user/cwe_report.txt` containing only these two CWE IDs, separated by a comma (e.g., `CWE-123, CWE-456`). Order does not matter.

**Phase 2: Secure Coding**
1. Fix the command injection vulnerability in `/home/user/rotate_cli.cpp`. Remove the `system()` call and use C++17's `std::filesystem` to perform the file copying securely. 
2. Fix the XSS vulnerability in the HTML report generation. Implement basic HTML entity encoding for the `status_msg` variable before writing it to the report (specifically, replace `<`, `>`, and `&` with `&lt;`, `&gt;`, and `&amp;`).
3. Overwrite `/home/user/rotate_cli.cpp` with your secured code.

**Phase 3: Credential Rotation**
1. Generate a new, self-signed RSA 2048-bit TLS certificate and private key.
2. Save the certificate to `/home/user/new_cert.pem` and the key to `/home/user/new_key.pem`.
3. The certificate must be valid for exactly 365 days and have a Subject Common Name (CN) of `localhost`.

**Phase 4: Compilation**
1. Compile your secured C++ program using the following command:
   `g++ -std=c++17 /home/user/rotate_cli.cpp -o /home/user/rotate_cli`
2. Ensure it compiles without errors.

*Notes:*
- Do not change the CLI arguments or the core logic of reading from the input configuration, just secure the file operations and HTML output.
- All operations should take place in `/home/user`.