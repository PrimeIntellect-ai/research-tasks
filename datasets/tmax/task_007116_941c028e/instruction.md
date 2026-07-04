You are an administrator managing user account records. You use a local Git repository to track changes, and a Git hook is supposed to log every time a batch of user updates is pushed. 

Currently, the logging system is broken. The `post-receive` Git hook calls a Python script (`/home/user/scripts/log_update.py`), but because the environment variables are different when the hook runs, the script writes its log output (`commits.log`) directly into the bare repository directory instead of the centralized logs directory.

Your task is to fix this configuration and set up some log management:

1. **Fix the Hook**: Update the Git hook at `/home/user/user_repo.git/hooks/post-receive` so that it exports the environment variable `LOG_DEST` set to `/home/user/logs/user_commits.log` right before executing the Python script. Ensure the `/home/user/logs` directory exists.
2. **Setup Symlink**: Create a directory `/home/user/public_logs/`. Inside it, create a symbolic link named `latest_commits.log` that points to the absolute path `/home/user/logs/user_commits.log`.
3. **Log Rotation Script**: Create a Python script at `/home/user/scripts/rotate.py`. When executed, this script must rename `/home/user/logs/user_commits.log` to `/home/user/logs/user_commits.log.bak` and create a new, empty `/home/user/logs/user_commits.log`.
4. **Trigger the Hook**: Change directory to your workspace at `/home/user/admin_workspace`. Create a file named `alice.json`, commit it, and push to the `master` branch of the origin repository to trigger the hook.

Ensure all paths are exact as requested.