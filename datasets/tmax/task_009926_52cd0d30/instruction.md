You are a forensics analyst responding to a compromised Linux host. The system was running a custom bash-based file upload service. We suspect the attacker exploited a vulnerability in this service to drop a malicious payload, modify SSH keys to establish persistence, and obfuscate sensitive evidence.

Your objective is to audit the compromised service, recover the obfuscated evidence, demonstrate how the attack occurred, and secure the system's SSH access.

Here is the current state of the system:
- `/home/user/upload_server.sh`: The vulnerable bash script that handled file uploads.
- `/home/user/uploads/`: The intended directory for uploaded files.
- `/home/user/payload.sh`: A malicious script left behind by the attacker that obfuscated the sensitive evidence.
- `/home/user/evidence.dat`: The obfuscated evidence file.
- `/home/user/.ssh/authorized_keys`: Contains the attacker's public key (they overwrote the original file).
- `/home/user/sshd_config_custom`: A local copy of the SSH daemon configuration.

Perform the following tasks using Bash and standard CLI tools:

1. **CWE Identification & Auditing:** Audit `/home/user/upload_server.sh` and identify the primary vulnerability class (use the standard CWE format, e.g., CWE-XXX). Write a patched version of the server to `/home/user/upload_server_patched.sh` that securely strips any directory traversal sequences (e.g., strictly allowing only alphanumeric characters and dots in the filename) before saving.
2. **Exploit Crafting (PoC):** Write a bash script at `/home/user/poc.sh` that demonstrates the vulnerability found in the original `upload_server.sh`. When executed, `poc.sh` should pass input to `upload_server.sh` (via standard input or however the script reads it) such that it successfully writes a file named `pwned.txt` into `/home/user/.ssh/`.
3. **Evidence Recovery:** Analyze `/home/user/payload.sh` to understand how the attacker obfuscated the evidence. Reverse the process to extract the original plaintext flag from `/home/user/evidence.dat`.
4. **SSH Hardening & Key Management:** 
   - Extract the attacker's public key from `/home/user/.ssh/authorized_keys`.
   - Clear `/home/user/.ssh/authorized_keys`.
   - Generate a new, secure Ed25519 SSH key pair for the user (save it to `/home/user/.ssh/id_ed25519` with no passphrase) and place the new public key into `/home/user/.ssh/authorized_keys`.
   - Modify `/home/user/sshd_config_custom` to harden it: set `PermitRootLogin` to `no` and `PasswordAuthentication` to `no`. Ensure no other instances of these directives exist with insecure values.

Finally, compile your findings into a JSON report at `/home/user/forensics_report.json` with the following exact structure:
```json
{
  "vulnerability_cwe": "CWE-XXX",
  "attacker_public_key": "ssh-rsa AAAAB3NzaC1yc2E...",
  "recovered_evidence": "flag{...}"
}
```