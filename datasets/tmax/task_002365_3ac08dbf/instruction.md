You are a backup operator testing the restore of a local deployment pipeline. A bare Git repository has been restored to `/home/user/restore.git`, and a local source checkout is located at `/home/user/app_src`. 

However, the restore test is failing. Your task is to fix the pipeline, implement a staged deployment, and configure a custom Python log rotator.

Perform the following steps:

1. **Fix the Pre-Receive Hook:**
   Whenever you try to push from `/home/user/app_src` to `/home/user/restore.git`, the push is rejected. The pre-receive hook (`/home/user/restore.git/hooks/pre-receive`) is a Python script intended to enforce that all commits during a restore test contain the string "RESTORE_TEST" in the commit message. However, the script has a deliberate bug causing it to fail silently or crash. Fix the Python script so it successfully allows pushes when the commit message contains "RESTORE_TEST", and rejects them otherwise.

2. **Implement Staged Deployment (Post-Receive Hook):**
   Create a bash script at `/home/user/restore.git/hooks/post-receive` (ensure it is executable). Upon a successful push, this hook must:
   - Check out the latest code to a staging directory: `/home/user/deploy/staging`
   - Immediately copy the contents of the staging directory to the production directory: `/home/user/deploy/prod`
   - Create a logs directory at `/home/user/deploy/prod/logs` if it doesn't exist.

3. **Develop a Python Log Rotator:**
   Create a Python script at `/home/user/rotate.py`. This script must:
   - Target the directory `/home/user/deploy/prod/logs/`.
   - Find `app.log`. If it exists, rotate it by shifting old logs up to a maximum of 3 backups (`app.log.2` becomes `app.log.3`, `app.log.1` becomes `app.log.2`, `app.log` becomes `app.log.1`).
   - Create a fresh, empty `app.log` file.
   - Any log file older than `app.log.3` should be discarded/overwritten.

4. **Execute the Pipeline:**
   - Commit the current code in `/home/user/app_src` with the message "RESTORE_TEST trigger".
   - Push the code to the `master` branch of `/home/user/restore.git`.
   - After the push succeeds and the post-receive hook deploys the code, simulate some log activity by running `echo "Log entry 1" > /home/user/deploy/prod/logs/app.log`.
   - Run your `/home/user/rotate.py` script.
   - Simulate more activity: `echo "Log entry 2" > /home/user/deploy/prod/logs/app.log`.
   - Run your `/home/user/rotate.py` script again.

Ensure all directories are created if they do not exist.