You are a capacity planner analyzing the resource usage of a multi-service application. The application components are supposed to write their logs to specific directories defined in a central configuration file. However, due to a simulated "connectivity" and configuration issue, one of the components is failing to log its data, and you need to analyze the current storage usage while implementing a log rotation strategy to prevent future disk exhaustion.

Your task consists of the following steps:

1. **Configuration Management & Diagnostics:**
   - Read the configuration file located at `/home/user/config/app_services.ini`.
   - The file defines three services (`service_alpha`, `service_beta`, and `service_gamma`), along with their target log directories and their assigned local ports.
   - One of the local ports defined in the config is currently active (a process is listening on it). Identify which port is open.
   - One of the services has a misconfigured log directory path that points to a non-existent `_offline` directory. Correct the configuration file to point to `/home/user/logs/service_gamma/` and create this directory.

2. **Log Capacity Analysis & Rotation Script:**
   - Write a Python script at `/home/user/analyze_capacity.py`.
   - When executed, the script must parse the corrected `/home/user/config/app_services.ini`.
   - For each service, the script must inspect its assigned log directory and calculate the total size (in bytes) of all files ending in `.log` BEFORE doing any rotation.
   - The script must perform log rotation: any `.log` file strictly larger than 1024 bytes must be renamed to have a `.archive` extension (e.g., `app.log` becomes `app.log.archive`), and a new, empty file with the original name (e.g., `app.log`) must be created.
   - Finally, the script must write a JSON report to `/home/user/capacity_report.json` with the exact following structure:
     ```json
     {
       "active_port": <integer_of_the_listening_port>,
       "storage_usage_bytes": {
         "service_alpha": <total_bytes>,
         "service_beta": <total_bytes>,
         "service_gamma": <total_bytes>
       }
     }
     ```

Run your script to produce the final `capacity_report.json` and ensure all rotations are complete.