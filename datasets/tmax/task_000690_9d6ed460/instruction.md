You are an incident responder investigating a recent breach on a Linux web server. The attacker left behind an encrypted payload and a custom Python module used for their Command and Control (C2) communications. They appear to be looking for privilege escalation vectors.

Your investigation is localized to the directory `/home/user/incident_042`.

**Available Evidence:**
1. `/home/user/incident_042/suspicious_payload.hex`: A hex-encoded ciphertext containing the attacker's next phase payload.
2. `/home/user/incident_042/crypto_module.py`: The custom encryption script the attacker used. It implements a stream cipher based on a Linear Congruential Generator (LCG) modulo 256. 

**Intelligence gathered:**
- The plaintext, before encryption, is a Base64 encoded JSON string.
- We know the underlying JSON payload begins with exactly this string: `{"cmd":"audit"`
- Therefore, the first several bytes of the *Base64 encoded plaintext* are known to you.

**Your Objectives:**

1. **Cryptanalysis & Decoding:**
   Write a Python script to perform a known-plaintext attack against the LCG cipher. You need to recover the initial seed (`X_0`), the multiplier (`a`), and the increment (`c`). Use these parameters to decrypt the entire payload, then Base64-decode it to reveal the JSON instructions.

2. **Privilege Escalation Auditing:**
   The decrypted JSON payload contains instructions the attacker was planning to execute, formatted roughly like: `{"cmd":"...", "dir":"...", "vuln":"..."}`.
   The `vuln` field specifies a type of misconfiguration the attacker is hunting for, and `dir` specifies the target directory.
   Write an auditing script in Python to scan the specified `dir` (recursively) for the vulnerability mentioned in `vuln`. 
   *Note: If `vuln` is `"world_writable"`, you must find all files in `dir` that have write permissions for "others" (e.g., `chmod o+w`).*

3. **Reporting:**
   Create a final report file at `/home/user/incident_042/report.json` with the following exact structure:
   ```json
   {
     "decrypted_payload": {
       "cmd": "<value>",
       "dir": "<value>",
       "vuln": "<value>"
     },
     "privesc_candidates": [
       "/absolute/path/to/file1",
       "/absolute/path/to/file2"
     ]
   }
   ```
   *Requirements for `report.json`:*
   - The `decrypted_payload` must be the parsed JSON object from the decrypted Base64 string.
   - The `privesc_candidates` list must contain absolute paths to the vulnerable files found during your audit, sorted alphabetically.

Complete these steps using Python and standard bash commands. All necessary files are present on the system.