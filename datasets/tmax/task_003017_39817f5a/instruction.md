You are a Cloud Architect migrating legacy storage monitoring services to a new environment. We have a legacy Python monitoring script that is supposed to run periodically to check filesystem statuses and remote backup connectivity. However, it is currently failing to write to the correct location because of environment variable differences when run in a non-interactive shell (like cron), and it doesn't correctly parse our custom mount configuration file.

Your task is to fix the monitoring setup, implement the missing diagnostic logic, and ensure the metrics are written to the correct destination.

Here are your requirements:

1. **The Configuration File:** 
   There is a mock fstab file located at `/home/user/migration/fstab_mock`. It contains space-separated lines with the following format:
   `<mount_point> <fs_type> <backup_service_port>`
   (e.g., `/home/user/data_vol1 ext4 8081`)

2. **The Python Script (`/home/user/migration/monitor.py`):**
   Write a Python script at `/home/user/migration/monitor.py` that does the following:
   - Reads `/home/user/migration/fstab_mock`.
   - For each `<mount_point>` defined in the file, checks if the directory exists. If it does not exist, the script must create it.
   - Performs a connectivity diagnostic: for each entry, attempt to establish a TCP connection to `localhost` on the specified `<backup_service_port>` with a 1-second timeout.
   - Reads the `LOG_DIR` environment variable. If `LOG_DIR` is not set, the script should default to `/tmp` (this simulates the bug we are trying to fix).
   - Writes a JSON report to a file named `status.json` inside the directory specified by `LOG_DIR`.

   The JSON format must strictly be a dictionary mapping the mount points to their status:
   ```json
   {
     "/home/user/data_vol1": {
       "fs_type": "ext4",
       "backup_reachable": true
     },
     "/home/user/data_vol2": {
       "fs_type": "xfs",
       "backup_reachable": false
     }
   }
   ```

3. **The Wrapper Script (`/home/user/migration/run_monitor.sh`):**
   To fix the path/environment issues typically encountered in our cron jobs, create an executable bash wrapper script at `/home/user/migration/run_monitor.sh`.
   This script must:
   - Explicitly export `LOG_DIR=/home/user/migration/logs`.
   - Ensure the `/home/user/migration/logs` directory exists.
   - Execute the `/home/user/migration/monitor.py` script.

4. **Execution:**
   Once you have created the files, execute `/home/user/migration/run_monitor.sh` so that the `/home/user/migration/logs/status.json` file is generated properly. 
   
Note: For testing, assume that a local service is listening on port `8081`, but port `8082` is closed. You must set up `/home/user/migration/fstab_mock` with exactly these two lines before running your scripts:
`/home/user/data_vol1 ext4 8081`
`/home/user/data_vol2 xfs 8082`

Ensure all directories, files, and permissions are correctly configured and the final JSON file matches the exact schema requested.