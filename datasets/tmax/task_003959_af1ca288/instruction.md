You are managing a mock CI/CD pipeline for a containerized microservices architecture. The deployment pipeline has failed due to incorrect file permissions and network timeouts between services. You need to investigate the logs, fix the permissions, and generate an automated report for the pipeline.

Perform the following steps:

1. **Fix Deployment Key Permissions**: 
   The mock CI/CD pipeline uses an SSH key located at `/home/user/deploy_keys/id_ed25519`. The pipeline currently refuses to run because the permissions are too open.
   - Set the permissions of the directory `/home/user/deploy_keys` to exactly `700`.
   - Set the permissions of the key file `/home/user/deploy_keys/id_ed25519` to exactly `600`.

2. **Process Network Logs**:
   The CI/CD test runner produced a network connectivity log at `/home/user/network_logs.txt`. 
   The log lines follow this exact format:
   `[YYYY-MM-DD HH:MM:SS] SOURCE:<service_name> TARGET:<target_name> PORT:<port> RESULT:<status>`
   
   Using standard shell text-processing tools (e.g., `awk`, `grep`, `sed`), extract the `SOURCE` service names for all entries where the `RESULT` is exactly `TIMEOUT`.
   - Save the extracted service names to `/home/user/failed_services.txt`.
   - The file must contain only the service names (one per line).
   - The list must be deduplicated (unique) and sorted alphabetically.

3. **Generate CI/CD Report (Python)**:
   Write and execute a Python script at `/home/user/build_report.py`.
   This script must:
   - Read the `/home/user/failed_services.txt` file you just created.
   - Generate a JSON file at `/home/user/ci_report.json`.
   - The JSON file must have the following exact structure:
     ```json
     {
       "pipeline_status": "failed",
       "failed_services": ["service_name_1", "service_name_2"]
     }
     ```
   (Where the array contains the contents of `failed_services.txt`).

Complete these tasks in the terminal. Your success will be verified by checking the permissions, the contents of `/home/user/failed_services.txt`, and the structure of `/home/user/ci_report.json`.