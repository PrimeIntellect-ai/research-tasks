You are a site administrator managing user accounts. We use a local bare Git repository at `/home/user/account_repo.git` to track user manifest files. 

Whenever an administrator pushes changes to this repository, a Python synchronization script located at `/home/user/scripts/sync_accounts.py` needs to run to process the updates. 

Recently, we noticed that the synchronization logs are being written to the wrong location (inside the bare Git repository's internal directories) instead of the designated log directory. This happens because Git hooks execute with a specific environment and working directory, and the Python script relies on the `LOG_DIR` environment variable to know where to write `sync.log`. If `LOG_DIR` is missing, it defaults to the current working directory.

Your task is to write a bash script at `/home/user/fix_hook.sh` that idempotently installs or updates the `post-receive` Git hook to fix this issue.

Requirements for `/home/user/fix_hook.sh`:
1. It must create or overwrite the file `/home/user/account_repo.git/hooks/post-receive`.
2. Ensure the hook file is executable.
3. The generated `post-receive` hook must:
   - Export the environment variable `LOG_DIR=/home/user/logs`.
   - Execute `/usr/bin/python3 /home/user/scripts/sync_accounts.py` in the background (so the `git push` command doesn't hang waiting for the script to finish).
   - Redirect both standard output and standard error of the Python script to `/home/user/logs/hook_output.log`.
4. Your `fix_hook.sh` script must be idempotent (running it multiple times should leave the system in the exact same correct state without errors).

Do not manually run the git push to test. Just create the `fix_hook.sh` script. The automated verification system will execute your script, perform a `git push` to the repository, and verify that `/home/user/logs/sync.log` and `/home/user/logs/hook_output.log` are created in the correct directory.