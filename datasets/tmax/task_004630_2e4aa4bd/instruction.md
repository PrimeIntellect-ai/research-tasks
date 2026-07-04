You have been assigned to audit a compromised internal web server environment. As a security auditor, your goal is to investigate the breach, identify the vulnerability, and implement a fix. You will need to process an intercepted audio file, analyze certificate chains, audit multi-language source code, and create a robust input filter.

Here are your instructions:

**Phase 1: Intelligence Gathering**
1. We intercepted a voicemail from the suspected insider threat. The audio file is located at `/app/intercepted_call.wav`.
2. Transcribe this audio file. The speaker mentions a specific "backdoor passphrase" used to generate malicious cryptographic assets. 

**Phase 2: Cryptographic Audit**
1. Navigate to `/home/user/audit/crypto_assets/`. You will find several SSH keys and X.509 certificate chains.
2. The attacker generated a rogue Root CA using the backdoor passphrase from the audio file as the key passphrase. 
3. Identify which certificate chain in `/home/user/audit/crypto_assets/certs/` is signed by this rogue CA. 
4. Identify the rogue SSH public key in `/home/user/audit/crypto_assets/ssh/` that has a comment containing the SHA256 hash of the backdoor passphrase.

**Phase 3: Vulnerability Analysis**
1. Review the web application source code located in `/home/user/audit/webapp/` (which contains both a Node.js frontend and a Python/Flask backend).
2. Identify the specific CWE (Common Weakness Enumeration) that allowed the attacker to compromise the system (e.g., CWE-22, CWE-78, CWE-89).

**Phase 4: Adversarial Filtering**
1. You must write a detection script located at `/home/user/filter.py` to act as a WAF (Web Application Firewall) for the vulnerability you identified.
2. The script must accept a single file path as a command-line argument: `python3 /home/user/filter.py <path_to_payload_file>`
3. The script must read the contents of the file and evaluate if it contains the exploit payload for the CWE you found.
4. If the payload is malicious, print exactly `REJECT` to stdout and exit with code 1.
5. If the payload is benign, print exactly `ACCEPT` to stdout and exit with code 0.

**Phase 5: Reporting**
Generate a JSON report at `/home/user/audit_report.json` with the following exact structure:
```json
{
  "backdoor_passphrase": "<passphrase extracted from audio>",
  "rogue_cert_file": "<filename of the rogue certificate chain, e.g., chain3.pem>",
  "rogue_ssh_key_file": "<filename of the rogue ssh pubkey, e.g., id_rsa_2.pub>",
  "identified_cwe": "<CWE ID, e.g., CWE-78>"
}
```