You are a Cloud Architect preparing to migrate a legacy filesystem and its associated background services to a new containerized environment. Before the migration begins, you need to create a bash-based monitoring tool to verify the environment's readiness, check storage limits, and ensure the target container instance is healthy.

Perform the following steps:

1. **Environment Setup**
   Create an environment configuration file at `/home/user/migration_env.sh`. It must export the following variables:
   - `TZ` set to `Asia/Tokyo`
   - `LC_ALL` set to `C`
   - `MAX_DISK_KB` set to `10240` (representing 10 MB)

2. **Storage Preparation**
   Create a directory at `/home/user/migration_data`.
   Inside this directory, create a file named `payload.bin` that is exactly 12288 KB (12 MB) in size containing zero bytes (e.g., using `dd`). 

3. **Container Lifecycle Management**
   Start a background Apptainer instance named `service_migrator` using the `docker://alpine:latest` image.

4. **Monitoring Script**
   Write a Bash script at `/home/user/check_readiness.sh` and make it executable. The script must:
   - Source the `/home/user/migration_env.sh` file.
   - Accept a single argument: a UNIX epoch timestamp (e.g., `1710000000`).
   - Format this timestamp into a date string using the format `YYYY-MM-DD HH:MM:SS`. Due to the sourced environment, this must evaluate in the `Asia/Tokyo` timezone.
   - Check if the Apptainer instance named `service_migrator` is currently running.
   - Calculate the total disk space used by `/home/user/migration_data` in kilobytes (KB). Use `du -sk` and extract just the integer.
   - Compare the disk usage against `MAX_DISK_KB`. If it is strictly greater than `MAX_DISK_KB`, the state is `EXCEEDED`, otherwise it is `OK`.
   - Output a single log line to standard output in exactly this format:
     `[{TIMESTAMP}] INSTANCE:{RUNNING|STOPPED} DISK_KB:{SIZE} LIMIT:{OK|EXCEEDED}`

5. **Execution**
   Run your script exactly as follows and redirect the output to `/home/user/final_status.log`:
   `/home/user/check_readiness.sh 1710000000 > /home/user/final_status.log`