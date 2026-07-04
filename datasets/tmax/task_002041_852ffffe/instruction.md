You are a Linux Systems Engineer tasked with hardening and managing application deployments. We need a robust Bash script that simulates a secure, rolling deployment system with built-in storage monitoring and primitive container-like process lifecycle management.

Write a Bash script at `/home/user/deploy.sh` that takes a single argument: the path to an application archive (`.tar.gz`). The script must perform the following actions securely and robustly:

1. **Initialization & Error Handling:** 
   - Use strict error handling (`set -euo pipefail`).
   - All deployments must occur within the base directory: `/home/user/app_storage/`. Create this directory if it does not exist.

2. **Storage Monitoring (Quota Check):**
   - Before extracting, calculate the current disk usage of `/home/user/app_storage/` in kilobytes.
   - If the usage exceeds 5000 KB (5 MB), the script must abort, print `ERROR: Storage quota exceeded`, and log the failure.

3. **Security Hardening (Static Analysis):**
   - Extract the archive to a temporary directory in `/home/user/app_storage/tmp_extract_$$`.
   - The archive will contain a file named `run.sh`. Read `run.sh` and check if it contains the strings `curl` or `wget`.
   - If either string is found, delete the temporary directory, abort the deployment, print `ERROR: Security violation detected`, and log the failure.

4. **Staged/Rolling Deployment:**
   - If the checks pass, rename the temporary directory to `/home/user/app_storage/app_<basename_of_tarball_without_extensions>`. (e.g., if deploying `v1.tar.gz`, the directory should be `app_v1`).
   - Execute the `run.sh` script from the new directory in the background. Redirect its stdout and stderr to `/home/user/app_storage/app.log`.
   - Read the PID of the newly started background process.
   - If a file exists at `/home/user/app_storage/current.pid`, read the old PID from it. Send a graceful termination signal (`SIGTERM`, kill -15) to the old PID to shut down the previous version.
   - Write the *new* PID to `/home/user/app_storage/current.pid`.

5. **Logging:**
   - Append a log entry to `/home/user/deploy.log` for every deployment attempt.
   - On success: `[SUCCESS] Deployed <tarball_name> with PID <pid>`
   - On failure: `[FAILED] <tarball_name> - <Reason>` (where Reason is either `Quota exceeded` or `Security violation`).

**Execution Phase:**
There are four pre-existing archives located in `/home/user/apps/`:
- `/home/user/apps/v1.tar.gz`
- `/home/user/apps/v2.tar.gz`
- `/home/user/apps/v3.tar.gz`
- `/home/user/apps/v4.tar.gz`

After writing the script, you must make it executable and run it sequentially on `v1.tar.gz`, `v2.tar.gz`, `v3.tar.gz`, and `v4.tar.gz` in that exact order to complete the task. Leave the final processes running.