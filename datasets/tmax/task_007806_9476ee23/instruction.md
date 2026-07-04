You are acting as a cloud architect migrating web and email services to a new infrastructure. 

A critical step in our CI/CD deployment pipeline involves running a Python validation script (`/home/user/validate_deployment.py`) that connects to our deployment targets and checks TLS configurations for our web and email servers. However, the pipeline is currently failing for two reasons:

1. **SSH Configuration Issue:** Our local deployment SSH configuration (`/home/user/.ssh/config`) is silently rejecting key-based logins to the `migration-target` host, causing the automated pipeline to hang or fail when it falls back to password authentication. 
2. **Brittle Python Script:** The `validate_deployment.py` script crashes completely when a referenced TLS certificate file for a service is missing, rather than catching the error and reporting it.

Your task is to fix both of these issues:

**Step 1: Fix the SSH Config**
Inspect `/home/user/.ssh/config`. Ensure that the configuration for the host `migration-target` allows public key authentication and explicitly uses the identity file `/home/user/.ssh/migration_key`. Remove or fix any directives that disable key-based login.

**Step 2: Fix the Python Validation Script**
Inspect `/home/user/validate_deployment.py`. It reads a manifest at `/home/user/services.json` containing web and email configurations. 
Modify the Python script to include robust error handling:
- It attempts to read the contents of the `tls_cert` file for each service.
- If the file does not exist, the script must catch the exception (do not let the script crash) and record the status for that service as `"MISSING_CERT"` in its output.
- If the file exists, it should record the status as `"OK"`.

**Step 3: Run the Script**
Execute the modified Python script. It is programmed to output its findings to `/home/user/report.json`. 

Ensure that:
- `/home/user/.ssh/config` is properly corrected.
- `/home/user/report.json` is generated successfully and formatted properly.