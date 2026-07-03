You are a deployment engineer rolling out an update for our internal email server staging environment. The deployment pipeline is currently broken due to an incorrectly configured filesystem structure, missing environment variables, and an SSH configuration that is silently rejecting key-based logins during the pre-flight connectivity diagnostics.

Perform the following tasks using Bash commands:

1. **Staged Deployment Filesystem Setup**: 
   The application resides in `/home/user/deploy`. 
   Create a directory structure for a rolling deployment:
   - Create the directory `/home/user/deploy/releases/v2.0`
   - Inside this directory, create a file named `mail_server.conf` containing exactly the string: `SMTP_HOST=staging.mail.internal`
   - Create a symbolic link at `/home/user/deploy/current` that points to the `/home/user/deploy/releases/v2.0` directory.

2. **Environment Variable Setup**:
   The deployment tools require specific environment variables to track the staging rollout.
   Append the following to `/home/user/.bash_profile` (create it if it doesn't exist):
   - `export DEPLOY_ENV=staging`
   - `export MAIL_CONFIG=/home/user/deploy/current/mail_server.conf`

3. **SSH Connectivity Fix**:
   The deployment script performs a connectivity diagnostic over SSH, but it is currently failing because key-based authentication is explicitly disabled in the local SSH client config.
   Modify the file `/home/user/.ssh/config` to change the line `PubkeyAuthentication no` to `PubkeyAuthentication yes`. (Assume the file and the line already exist, just edit it in place).

4. **Verification Log**:
   To prove the deployment environment is ready, generate a report file at `/home/user/deployment_report.log` with exactly two lines:
   - The first line should be the absolute path that the symlink `/home/user/deploy/current` resolves to (use `readlink -f /home/user/deploy/current`).
   - The second line should be the output of searching for the `PubkeyAuthentication` configuration in the ssh config file (e.g., `grep PubkeyAuthentication /home/user/.ssh/config | xargs`).

Do not run the actual deployment script; just ensure the environment and configuration files are correctly prepared.