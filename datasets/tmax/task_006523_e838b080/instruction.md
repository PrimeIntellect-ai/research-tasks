I need you to fix a deployment issue for my simulated background services. The system frequently fails because the log directory fills up, and the environment variables are not correctly configured for the application launcher. 

You need to perform the following steps to build a robust launch mechanism:

1. **Environment Profile Setup:**
   Create a file at `/home/user/.env_profile`. Inside it, define and export two environment variables:
   - `APP_PORT` set to `8080`
   - `APP_ENV` set to `production`

2. **Storage Monitoring Script:**
   Write a script at `/home/user/monitor_storage` (you may use any language like Python, Bash, Ruby, etc., but ensure it has execute permissions and a valid shebang). 
   This script must:
   - Accept exactly one argument: the path to a directory.
   - Robustly check if the directory exists. If it does not, it must print "Error: Directory not found" to standard error (stderr) and exit with status code `1`.
   - Calculate the total size of all files within the specified directory (in bytes).
   - If the total size strictly exceeds 1,000,000 bytes (1 MB), the script must delete all files ending with `.old` in that directory, and print exactly `STATUS: CLEANED` to standard output (stdout).
   - If the total size is 1,000,000 bytes or less, it should not delete anything and print exactly `STATUS: OK` to stdout.
   - Exit with status code `0` upon successful execution.

3. **Application Launcher:**
   Create a robust shell script at `/home/user/run_app.sh` (ensure it is executable) that orchestrates the startup:
   - It must enable strict error handling (e.g., `set -e` in Bash) so it fails immediately if any command fails.
   - It must source the `/home/user/.env_profile` file.
   - It must execute your storage monitoring script, passing `/home/user/app_logs` as the argument.
   - If the monitoring script succeeds, the launcher must append exactly the following line to `/home/user/app_status.log`:
     `[SUCCESS] Environment $APP_ENV initialized on port $APP_PORT`
     *(Make sure the variables are evaluated in the output).*

To test your implementation, ensure all scripts are created with the correct permissions, and then execute `/home/user/run_app.sh`.