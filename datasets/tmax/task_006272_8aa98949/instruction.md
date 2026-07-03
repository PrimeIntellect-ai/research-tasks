As a compliance analyst, you are tasked with generating a secure audit trail for a legacy application environment. You must perform a security assessment on the environment and securely log your findings using a Rust application.

Follow these steps:
1. **Binary Analysis & Password Cracking:** Analyze the ELF binary located at `/home/user/legacy_system/auth_bin`. Somewhere inside this binary is a hardcoded password hash labeled with the prefix `HASH:` (e.g., `HASH:abcdef...`). This is an MD5 hash of a 4-digit numeric PIN. Extract the hash and crack it to find the original 4-digit PIN.
2. **Vulnerability Analysis:** Review the source code of the Rust web server located in `/home/user/web_server/src/main.rs`. Identify the specific URL query parameter name that is used to redirect users after a successful login, which currently suffers from an Open Redirect vulnerability.
3. **Privilege Escalation Auditing:** Inspect the directory `/home/user/bin/`. There are several binaries here, but exactly one of them has the SUID bit set, posing a potential privilege escalation risk. Identify the name of this binary.
4. **Secure Audit Logging:** You have been provided a skeleton Rust project at `/home/user/audit_logger`. You must write the implementation for `src/main.rs` to encrypt your findings.
   - Construct a plaintext string exactly in this format: `PIN: <cracked_pin>, Redirect: <parameter_name>, SUID: <binary_name>` (e.g., `PIN: 9999, Redirect: return_to, SUID: suid_helper`).
   - Encrypt this plaintext using the `aes-gcm` crate (AES-128-GCM). Use the hardcoded key and nonce provided in the skeleton code.
   - Write the resulting raw ciphertext (with the MAC/authentication tag appended, which is the default behavior of `aes-gcm`) to `/home/user/audit_report.bin`.

Compile and run your Rust program to generate `/home/user/audit_report.bin`.