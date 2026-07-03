You are a Linux systems engineer responsible for hardening configurations and automating legacy deployments.

We have a legacy interactive deployment script at `/home/user/legacy_deploy.sh` that is prone to random crashes and requires manual interactive input. You need to write a Python-based supervisor script that automates this deployment, enforces configuration hardening, monitors storage space, and implements a restart policy.

Create a Python script at `/home/user/deploy_supervisor.py` that performs the following tasks in order:

1. **Storage Monitoring**: Check the available free space on the `/home/user/data` directory using Python's standard libraries. If the available space is less than 1024 bytes, write "ERROR: Insufficient space" to `/home/user/deploy.log` and exit immediately.
2. **Configuration Management**: Read the existing configuration file at `/home/user/app.conf`. Locate the line `insecure_mode=true` and change it to `insecure_mode=false`. Write the updated contents back to `/home/user/app.conf` safely.
3. **Interactive Automation & Supervision**: 
    - Use Python's `pexpect` module to spawn and control the `/home/user/legacy_deploy.sh` script.
    - The legacy script will prompt: `Enter hardening passphrase: `
    - Your script must automatically send the passphrase: `S3cr3tH4rd3n!`
    - The legacy script is unstable and may exit with a non-zero status code. Implement a supervisor restart policy: if the process crashes (exit code != 0), catch it and restart the process. You must retry up to a maximum of 5 total attempts.
    - If the script eventually succeeds (exit code 0), capture its final standard output line (excluding the passphrase prompt) and append it to `/home/user/deploy.log`.
    - If it fails 5 times, write "ERROR: Max retries reached" to `/home/user/deploy.log` and exit.

Requirements:
- Ensure your Python script is executable (`chmod +x`).
- Execute your script so that the `app.conf` is modified and `deploy.log` is generated successfully.
- You can install `pexpect` via `pip` if it is not already available.