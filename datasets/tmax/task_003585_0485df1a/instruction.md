You are a penetration tester and security engineer tasked with auditing and securing a local web application and its deployment environment. You need to identify a vulnerability, fix the Rust source code, harden the SSH configuration, and fix file permissions. Finally, you will summarize your findings in a JSON report.

Here are your specific objectives:

1. **Vulnerability Audit and Code Fix (Rust)**
   There is a Rust project located at `/home/user/web_service`. Inside `src/main.rs`, there is a function `read_user_file(filename: &str) -> Result<String, String>` that is intended to read files *only* from a specific public uploads directory. However, it is currently vulnerable to a classic web security flaw that allows attackers to read arbitrary files by manipulating the input path.
   - Audit `src/main.rs` and identify the Common Weakness Enumeration (CWE) identifier for this vulnerability.
   - Fix the vulnerability in `src/main.rs`. Modify `read_user_file` so that if the `filename` contains the `/` character or the `..` sequence, it immediately returns `Err("Invalid filename".to_string())`.
   - Ensure the project compiles and passes its tests by running `cargo test` in `/home/user/web_service`.

2. **SSH Hardening**
   A mock SSH server configuration file is located at `/home/user/ssh_audit/sshd_config`. It contains insecure default settings.
   - Modify `/home/user/ssh_audit/sshd_config` to strictly disable root login and disable password-based authentication. Update the existing configuration directives accordingly.

3. **Access Control / Key Management**
   An SSH private key used for deployment is stored at `/home/user/ssh_keys/id_rsa`. Its current permissions are dangerously open.
   - Fix the permissions of `/home/user/ssh_keys/id_rsa` to the standard, secure file permission required by SSH for private keys (read and write for the owner only).

4. **Audit Report**
   Create a final summary report at `/home/user/audit_report.json` with the following strict schema:
   ```json
   {
     "identified_cwe": "CWE-XXX",
     "ssh_root_login_fixed": true,
     "ssh_password_auth_fixed": true,
     "key_permission_octal": "0XXX"
   }
   ```
   *Replace `CWE-XXX` with the standard CWE identifier (e.g., CWE-79, CWE-22, etc.) for the vulnerability you fixed in the Rust code.*
   *Replace `0XXX` with the 4-digit octal permission you set for the SSH private key (e.g., "0644", "0600").*