You are a DevSecOps engineer tasked with enforcing "Policy as Code" for a new application deployment. 

The deployment package is located in `/home/user/deployment/`. You need to audit the components and generate a security compliance report.

Here are your auditing objectives:
1. **File Integrity Verification:** A manifest file `/home/user/deployment/manifest.sha256` contains the expected SHA-256 hashes of the files. Verify the integrity of all files listed in this manifest. Record any files that fail the integrity check.
2. **SSH Hardening Check:** Review the `/home/user/deployment/sshd_config` file. For the SSH configuration to be considered "hardened" (compliant), it must explicitly set both `PermitRootLogin no` AND `PasswordAuthentication no`. If either is missing or set to `yes`, it is not hardened.
3. **Certificate Chain Validation:** The deployment includes a server certificate `/home/user/deployment/cert.pem` and a trusted Certificate Authority file `/home/user/deployment/ca.pem`. Validate if `cert.pem` is properly signed and issued by `ca.pem`.
4. **CWE Identification:** Perform a code audit on `/home/user/deployment/app.py`. Identify the specific CWEs (Common Weakness Enumerations) present in the code. Look specifically for OS Command Injection (CWE-78) and Use of Hard-coded Credentials (CWE-798).

Write the results of your audit into a strictly formatted JSON file at `/home/user/policy_report.json`. The JSON file must have exactly the following schema:

```json
{
  "ssh_hardened": <boolean>,
  "cert_valid": <boolean>,
  "corrupted_files": ["<filename1>", "<filename2>"],
  "identified_cwes": ["<CWE-XXX>", "<CWE-YYY>"]
}
```

Constraints:
- `corrupted_files` should only contain the base filenames (e.g., "file.txt") of the files that failed the hash check.
- `identified_cwes` should be a list of strings formatted exactly as "CWE-78" or "CWE-798" if you find them in `app.py`. Sort the CWE list alphabetically.