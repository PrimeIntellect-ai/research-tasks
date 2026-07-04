You are a cloud architect migrating a legacy batch service to a new containerized environment. As part of our interim CI/CD workflow, we need a lightweight deployment and execution pipeline script written in Python to ensure the legacy code runs securely and with the correct environment context.

Your task is to create a Python script at `/home/user/run_pipeline.py` that acts as this mini-pipeline. When executed, your script must perform the following actions:

1. **Environment Preparation:**
   - Create the directory `/home/user/deploy/` and a subdirectory `/home/user/deploy/logs/`.
   - Copy the existing legacy artifact from `/home/user/source/legacy_batch.py` to `/home/user/deploy/active_batch.py`.

2. **Permission and ACL Management:**
   - Change the standard Unix permissions of `/home/user/deploy/active_batch.py` to `0500` (read and execute for the owner only, nothing for group/others).
   - Apply an Access Control List (ACL) to `/home/user/deploy/logs/` so that any *new* files created inside it automatically inherit default ACLs granting `rw-` (read and write) to the owner, and `---` (no permissions) to group and others. You may use the `setfacl` command via a subprocess.

3. **Locale and Timezone Configuration (Execution context):**
   - The legacy script relies heavily on specific timezone and locale behaviors. Your Python pipeline must execute `/home/user/deploy/active_batch.py` in a subprocess.
   - You must inject the following environment variables into the subprocess:
     - `TZ` set to `Pacific/Fiji`
     - `MIGRATION_LOCALE` set to `C.UTF-8`
     - Do not modify the system-wide timezone or locale; only apply these to the subprocess environment.

4. **Execution and Verification:**
   - The legacy script will automatically write a report to `/home/user/deploy/logs/execution.log` if the environment, file permissions, and directory ACLs are correct.
   - Run your `/home/user/run_pipeline.py` script to trigger the deployment and execution. 
   - Ensure that the execution completes successfully and `/home/user/deploy/logs/execution.log` is generated.