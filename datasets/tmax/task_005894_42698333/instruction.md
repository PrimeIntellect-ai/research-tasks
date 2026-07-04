You are an incident responder investigating a compromised custom C++ web authentication module. Attackers have been exploiting an open redirect vulnerability in the login flow to steal credentials and redirect users to malicious sites. 

You have been provided with the following files in `/home/user/`:
1. `/home/user/auth_handler` - The stripped ELF executable of the vulnerable authentication module.
2. `/home/user/auth_handler.cpp` - The source code for the module. Note: The source code contains a placeholder for a secret key (`SECRET_KEY_PLACEHOLDER`). The actual secret key was injected during compilation and is embedded directly inside the `auth_handler` binary.

Your task consists of the following steps:

1. **Vulnerability Identification:** Analyze the source code and identify the standard MITRE CWE identifier for the open redirect vulnerability present in the code.
2. **Binary Analysis:** Extract the hardcoded secret key from the compiled `/home/user/auth_handler` ELF binary.
3. **Token Forgery (Remediation Testing):** Write a C++ program at `/home/user/forge.cpp`. This program must implement the exact token generation logic found in `auth_handler.cpp` to create a valid authorization token for the specific URL: `https://secure.internal.com`. Use the secret key you extracted from the binary.
4. **Execution and Output:** 
   - Compile your C++ program and output the generated token to a file named `/home/user/safe_token.txt`.
   - Set the file permissions of `/home/user/safe_token.txt` to strictly `0600` (read and write for the owner only).
5. **Reporting:** Create a report file at `/home/user/incident_report.txt` with exactly the following format:
   ```
   CWE: CWE-XXX
   Secret: <extracted_secret_key>
   ```
   (Replace `XXX` with the correct numbers, and `<extracted_secret_key>` with the exact string found in the binary).

Ensure all requested files are created at the exact specified paths.