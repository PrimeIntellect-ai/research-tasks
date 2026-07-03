You are a DevSecOps engineer responsible for enforcing "policy as code" for a legacy web application. 

The application source code is located in `/home/user/app_code`. Your team uses a proprietary, closed-source security evaluator located at `/app/sec_eval` (a stripped binary) to score the security posture of the application's configuration.

Your task is to write a Python script at `/home/user/generate_policy.py` that analyzes the application code and generates a hardened security policy file named `policy.json` in the current working directory. The script must be completely autonomous, as it will be run in a CI/CD pipeline against different application codebases.

Your Python script must perform the following tasks:
1. **File Integrity Verification:** Scan all `.js` files in `app_code/static/` and compute their SHA-384 Subresource Integrity (SRI) hashes.
2. **Content Security Policy Enforcement:** Analyze the HTML files in `app_code/templates/` to determine the minimum required `script-src` directives. Generate a strict CSP string that avoids `'unsafe-inline'` by including the SHA-256 hashes of any inline scripts found in the templates. 
3. **Privilege Escalation & CWE Auditing:** Scan all files in `app_code/` for insecure permissions that could lead to privilege escalation. Flag any files that are world-writable or have the SUID bit set. Map these to "CWE-732" (Incorrect Permission Assignment for Critical Resource).

The script must write to `policy.json` with the following exact structure:
```json
{
  "sri_hashes": {
    "filename.js": "sha384-<base64_hash>"
  },
  "csp": "default-src 'self'; script-src 'self' 'sha256-<hash1>' 'sha256-<hash2>';",
  "vulnerabilities": [
    {
      "file": "relative/path/to/file",
      "cwe": "CWE-732",
      "issue": "world-writable" 
    }
  ]
}
```
*(Note: "issue" should be either "world-writable" or "suid-set" depending on the finding).*

You can run `/app/sec_eval policy.json` to see how your generated policy scores (it outputs a float between 0.0 and 1.0). 

Your goal is to iteratively refine your `/home/user/generate_policy.py` script so that it produces a `policy.json` that scores as close to 1.0 as possible on the current codebase.

Automated tests will evaluate your solution by running your Python script against a hidden, held-out application directory, and then running the `sec_eval` binary on your output. You must achieve a high score to pass.