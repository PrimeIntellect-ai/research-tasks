You are acting as a penetration tester analyzing a custom internal tool. You have been provided with the source code and configuration files of a system utility in the `/home/user/target_system` directory.

Your task is to audit this system, identify the vulnerabilities, and generate a programmatic report using Rust.

Perform the following steps:

1. **Cryptographic Verification**: The directory `/home/user/target_system/releases.txt` contains a list of SHA256 hashes and corresponding version numbers for the tool. Calculate the SHA256 hash of the source code file located at `/home/user/target_system/src/main.rs` and determine its exact version string from `releases.txt`.

2. **Vulnerability Analysis**: Analyze the Rust source code in `/home/user/target_system/src/main.rs`. Identify the exact type of injection vulnerability present (e.g., `sql_injection`, `command_injection`, `xss`, `log_injection`). 

3. **Privilege Escalation Auditing**: Review the deployment configuration file at `/home/user/target_system/config/sudoers_rules`. Identify the specific target user account that an attacker could escalate privileges to by exploiting the vulnerability in this tool.

4. **Proof of Concept**: Develop a proof-of-concept payload. If this payload were passed as the primary argument to the vulnerable program, it must successfully execute the command `whoami > /tmp/pwned` while ensuring the rest of the original command does not cause a syntax error that prevents execution (e.g., by commenting out the remainder).

5. **Reporting**: Write a Rust program at `/home/user/generate_report.rs`. When compiled and executed, your program must create a JSON file at `/home/user/vuln_report.json` with the following exact keys and your discovered values:
   - `"version"`: The version string of the audited source file.
   - `"vulnerability"`: The type of injection vulnerability found (lowercase).
   - `"escalation_user"`: The username you can escalate privileges to.
   - `"poc_payload"`: The exact payload string you developed in step 4.

Constraints:
- You must write the report generator in Rust.
- Your payload must use the `#` character to comment out trailing invalid bash syntax if necessary.
- Do not attempt to exploit a live system; only write the report.