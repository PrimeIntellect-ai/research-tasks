You are a system administrator tasked with diagnosing why a mock local system service is failing to deploy in our CI/CD pipeline environment.

We have a local deployment script located at `/home/user/deploy.sh`. When executed, it is supposed to start our background application runner. However, the deployment currently fails with an exit code of 1.

Your investigation and remediation must cover the following steps:

1. **Diagnose the deployment failure**:
   Execute `/home/user/deploy.sh` and determine why the service refuses to start. The issue is related to a simulated storage quota being exceeded in the `/home/user/app/data` directory.

2. **Fix the cleanup pipeline**:
   The directory is bloated with old log files. There is a cleanup script at `/home/user/bin/cleanup.sh` that is supposed to read `/home/user/app/registry.txt`, find all files marked with the status `PROCESSED`, delete those files from `/home/user/app/data/`, and update `registry.txt` to remove those entries.
   However, `cleanup.sh` is currently broken and fails to parse the file or delete the logs. 
   Rewrite or fix `/home/user/bin/cleanup.sh` using a text processing pipeline (`awk`, `sed`, `grep`, etc.) so that it successfully performs these actions. 
   *Note: The `registry.txt` file is formatted as `YYYY-MM-DD | filename.log | STATUS`.*

3. **Verify Deployment**:
   After fixing and running the cleanup script, run `/home/user/deploy.sh` again. It must succeed and exit with code 0.

4. **Scheduled Task Configuration**:
   To prevent this in the future, install a user cron job that runs `/home/user/bin/cleanup.sh` exactly at the top of every hour (e.g., 1:00, 2:00). 

5. **Reporting**:
   Once successful, create a file at `/home/user/resolution.txt` containing exactly two lines:
   - Line 1: The full path of the largest log file that was deleted.
   - Line 2: The exact cron expression you used.

Ensure all file permissions remain executable where applicable. You may use Bash, Python, or standard shell utilities to fix the cleanup script.