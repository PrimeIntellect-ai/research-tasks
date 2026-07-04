You are a Linux systems engineer responsible for setting up a hardened, local Git repository to store sensitive network configuration backups. You need to configure the environment, establish a simulated disk quota system for the repository, and set up the directory structure.

Please perform the following steps:

1. **Directory and Link Structure**: 
   Create a bare Git repository located at `/home/user/net-conf.git`. 
   Create a symbolic link at `/home/user/active-repo` that points to the bare repository directory.

2. **System Config Management**: 
   Create a configuration directory `/home/user/.config` if it doesn't exist. Inside it, create a file named `repo_quota` that contains exactly the number `2048` (representing a 2048 KB limit) and nothing else.

3. **Shell Profile Setup**: 
   Configure the user's shell profile by appending the following environment variables to `/home/user/.bash_profile`:
   - `GIT_AUTHOR_NAME="SysAdmin"`
   - `GIT_AUTHOR_EMAIL="sysadmin@local"`
   - `NETWORK_ENV="hardening"`

4. **Git Server and Storage Monitoring Hook**: 
   Create a `pre-receive` hook inside the bare repository. This script must act as a custom storage quota monitor. 
   Every time a push is attempted, the hook must:
   - Read the quota limit from `/home/user/.config/repo_quota`.
   - Calculate the total disk space currently used by the bare repository (in kilobytes) using `du -sk .` (assuming the hook runs from within the repository directory).
   - If the used space exceeds the quota, print exactly `QUOTA EXCEEDED` to standard error (`stderr`) and exit with a non-zero status to reject the push.
   - Otherwise, exit with a status of `0`.
   Make sure the hook file has the correct executable permissions.

5. **Verification Log**: 
   Once the setup is complete, create a file named `/home/user/completion.log` with exactly three lines:
   - Line 1: The absolute path of the target that `/home/user/active-repo` points to.
   - Line 2: The absolute path to the `pre-receive` hook file you created.
   - Line 3: The octal permissions of the `pre-receive` hook file (e.g., `755`).

Ensure all paths are absolute and exactly as specified. Do not require root access for any of these operations.