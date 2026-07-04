You are a DevSecOps engineer tasked with implementing a Policy-as-Code enforcement pipeline to validate internal application deployments. 

Your task is to write a multi-language enforcement tool (using Bash and Python) that evaluates a set of localized application repositories before they are permitted to deploy. 

There are three mock project repositories located in `/home/user/projects/`:
- `/home/user/projects/project_alpha/`
- `/home/user/projects/project_beta/`
- `/home/user/projects/project_gamma/`

Each project directory contains:
1. `deploy_token.jwt` - A JSON Web Token requesting deployment authorization.
2. `source_code/` - A directory containing application source code.
3. `deploy.sh` - The deployment script.

You must create a tool that performs the following three checks on each project:

**1. Token Generation and Validation**
Write a Python script to validate the `deploy_token.jwt` using the public key located at `/home/user/platform_pub.pem`. 
- The JWT must be valid (properly signed).
- The JWT must not be expired.
- The JWT payload must contain the claim `"deploy_role": "platform_admin"`.
If any of these conditions fail, the check fails with the reason `"invalid_token"`.

**2. Automated Vulnerability Scanning**
Implement a scanner to check all files inside the `source_code/` directory for hardcoded secrets. 
- Specifically, search for any string matching the regular expression for a mock API key: `MOCK_SEC_[a-zA-Z0-9]{16}`.
If found, the check fails with the reason `"hardcoded_secrets_found"`.

**3. Privilege Escalation Auditing**
Audit the `deploy.sh` script for risky commands that could lead to privilege escalation or insecure permissions.
- Flag the project if the script contains the exact string `chmod 777`.
- Flag the project if the script contains the exact string `sudo su` or `sudo bash`.
If found, the check fails with the reason `"privilege_escalation_risk"`.

**Output Requirements:**
Create a master script at `/home/user/run_policy.sh` that executes these checks. The final output must be written to exactly `/home/user/enforcement_results.json`. 

The JSON file must have the following exact structure:
```json
{
  "project_alpha": {
    "status": "pass_or_fail",
    "reasons": ["list", "of", "reasons", "if", "failed"]
  },
  "project_beta": { ... },
  "project_gamma": { ... }
}
```
*Note: If a project passes all checks, `"status"` should be `"pass"` and `"reasons"` should be an empty list `[]`. If it fails one or more checks, `"status"` should be `"fail"` and `"reasons"` must include the failure strings defined above ("invalid_token", "hardcoded_secrets_found", "privilege_escalation_risk") in alphabetical order.*

You may install any necessary Python packages (e.g., `PyJWT`, `cryptography`) using `pip install` in the user environment or a virtual environment.