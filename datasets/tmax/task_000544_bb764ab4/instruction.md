You are the site administrator for a platform that automatically provisions user accounts via email requests. The system consists of multiple microservices that have become misconfigured, and it lacks proper sanitization, making it vulnerable to malicious account names and spam. 

Your task is to fix the service configuration, write a robust email filter, and create an idempotent account scaffolding script.

**1. Service Configuration (Multi-Service Composition)**
The system runs two services located in `/home/user/app/services/`:
- `smtp_gateway.py`: A local SMTP server listening on port 10025. It receives emails, runs a filter, and if accepted, sends a webhook.
- `account_api.py`: A REST API listening on port 8080 that handles the final account creation database step.

Currently, they are failing to communicate. Modify `/home/user/app/services/config.json` so that the `smtp_gateway` correctly points its `webhook_url` to the `account_api` endpoint (`http://127.0.0.1:8080/provision`). Also ensure `account_api` is configured to bind to `127.0.0.1` and not `0.0.0.0`.

**2. The Email Filter (Adversarial Robustness)**
The `smtp_gateway` needs a filter script to block malicious or malformed requests. 
Write a Python script at `/home/user/app/filter.py`. It will be invoked via CLI with a single argument: the path to an email text file.
Invocation: `python3 /home/user/app/filter.py <path_to_email_file>`

Rules for a VALID account request (must exit with code `0`):
- The email must have a header: `Subject: Request Account: <username>`
- The `<username>` must be exactly 3 to 12 characters long and consist ONLY of lowercase letters and numbers (no spaces, hyphens, or uppercase).
- The email body MUST contain the exact phrase: `I accept the terms of service.` (case-insensitive).

Rules for an INVALID request (must exit with code `1`):
- Any violation of the above.
- Any directory traversal attempts in the username (e.g., `../`, `/`).
- Any shell metacharacters in the username.

**3. Account Scaffolding & Storage Management**
The `account_api.py` triggers a shell script when an account is approved.
Create this script at `/home/user/app/create_skel.sh`. It must take one argument (the username) and do the following idempotently:
1. Calculate the current size of the `/home/user/accounts/` directory in bytes (using `du -sb`). If it exceeds 5000000 bytes (5MB), print exactly `QUOTA_EXCEEDED` to stdout and exit with code 2.
2. Create the directory `/home/user/accounts/<username>/storage/`.
3. Create a symbolic link at `/home/user/accounts/<username>/shared` pointing to the existing directory `/home/user/shared_data/`.
4. Create a config file `/home/user/accounts/<username>/user.conf` containing the text `status=active`. If it already exists, do not overwrite it.

Make sure the bash script is executable. You can start the services manually or write an auxiliary script to run them in the background while you test.