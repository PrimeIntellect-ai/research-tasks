As a DevSecOps engineer, you are tasked with enforcing SSH security policies by analyzing authentication logs and identifying weak keys and malicious IPs. 

We have a proprietary log analysis package vendored at `/app/ssh_log_analyzer-1.0.0.tar.gz`. However, the package has a bug in its regular expression parsing for SSH key fingerprints and IP extraction, causing it to drop valid log entries. 

Your task is to:
1. Extract and fix the `ssh_log_analyzer` package so that it correctly parses SSH log lines. The bug is located in the `parser.py` file where the regex fails to account for modern ECDSA/Ed25519 key fingerprint formats and IPv6 addresses.
2. Install your fixed version of the package.
3. Write a script `/home/user/enforce_policy.py` (in a language of your choice, though Python is recommended to easily use the package) that reads `/home/user/auth.log`.
4. Your script must identify all IP addresses that have attempted to log in with a known compromised key fingerprint (which you must identify by checking against a list of weak MD5/SHA256 hashes you will generate from the CWE audit rules in `/home/user/cwe_rules.json`).
5. Your script must output a file `/home/user/threat_report.json` containing a list of malicious IPs and weak key fingerprints.

Format of `/home/user/threat_report.json`:
```json
{
  "malicious_ips": ["192.168.1.100", "2001:db8::1"],
  "weak_keys": ["SHA256:abcd123...", "MD5:de:ad:be:ef..."]
}
```

Ensure your logic is accurate. Your threat report will be evaluated against a secret ground truth of actual malicious IPs and weak keys present in the logs. You must achieve an F1 score of at least 0.95.