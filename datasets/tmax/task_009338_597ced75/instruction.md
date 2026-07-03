You are a DevSecOps engineer responsible for enforcing security policies as code. You need to create a custom pre-deployment security scanner written in Rust that audits a target web application repository before deployment.

The repository is located at `/home/user/repo`. 

Your task is to write a Rust project in `/home/user/policy-scanner` that performs three specific checks and writes a JSON report to `/home/user/policy_report.json`.

Here are the requirements for your Rust scanner:

1. **Intrusion/Vulnerability Detection (Pattern Matching):**
   The web application handles login flows in `/home/user/repo/src/auth.js`. You must scan this file for an open redirect vulnerability. Specifically, check if the code dynamically redirects to a query parameter without validation (look for the regex pattern `res\.redirect\(.*req\.query\.(return_to|next).*\)`).

2. **Certificate Chain Validation:**
   The repository contains a staging server certificate at `/home/user/repo/certs/server.crt` and the internal Root CA at `/home/user/repo/certs/ca.crt`. Your Rust program must validate that `server.crt` is properly signed by `ca.crt`. You may use `std::process::Command` to invoke standard Linux CLI tools (like `openssl`) from within your Rust code to perform this check.

3. **File Integrity Verification:**
   The deployment manifest is located at `/home/user/repo/deploy.yaml`. Its expected SHA-256 hash is stored in `/home/user/repo/deploy.yaml.sha256` (formatted as `<hash>  deploy.yaml`). Your Rust program must compute the SHA-256 hash of `deploy.yaml` natively using the `sha2` crate and verify if it matches the hash in the `.sha256` file.

**Output Specification:**
After completing these checks, your Rust program must output a JSON file to `/home/user/policy_report.json` with the following exact structure:
```json
{
  "open_redirect_found": <boolean>,
  "cert_valid": <boolean>,
  "integrity_valid": <boolean>
}
```

**Steps to complete:**
1. Create the Rust project in `/home/user/policy-scanner`.
2. Add necessary dependencies (e.g., `regex`, `sha2`, `serde`, `serde_json`) to your `Cargo.toml`.
3. Write the Rust code to perform the three checks.
4. Compile and run your tool to generate `/home/user/policy_report.json`.