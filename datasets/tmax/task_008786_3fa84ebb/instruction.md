You are an engineer tasked with implementing a CI/CD test pipeline for a new backup operator system. Our system relies on two Rust components: a mock data storage service (`storage_service`) and a backup restore client (`restore_client`). Currently, the automated test is failing due to a network misconfiguration and missing application-level user credentials.

Your task is to fix the application code, create the required user credential file, and write an interactive bash pipeline script to orchestrate the test.

Here is what you need to do:

1. **Fix the Network Misconfiguration:**
   The `restore_client` in `/home/user/backup_op/restore_client/src/main.rs` is hardcoded to connect to `127.0.0.1:9090`. However, the `storage_service` binds exclusively to the loopback alias `127.0.0.2:9090` to simulate cross-network isolation. Update the Rust source code of `restore_client` to connect to the correct IP.

2. **Application User Administration:**
   The `storage_service` requires an application user configuration file to authorize the restore operation. Create a JSON file at `/home/user/backup_op/users.json` with the following structure:
   ```json
   {
     "users": [
       {
         "username": "backup_agent",
         "group": "system_admins",
         "token": "pipeline-token-883"
       }
     ]
   }
   ```

3. **Construct the CI/CD Pipeline Script:**
   Write a bash script at `/home/user/backup_op/run_pipeline.sh`. This script must:
   - Include `#!/bin/bash` at the top.
   - Change directory to `/home/user/backup_op`.
   - Build both Rust projects (`storage_service` and `restore_client`) using `cargo build --release`.
   - Start the `storage_service` executable in the background (`./storage_service/target/release/storage_service`).
   - Wait for 2 seconds to allow the service to start.
   - Run the `restore_client` executable, passing the authentication token as an argument and directing the output to a log file: `./restore_client/target/release/restore_client --token pipeline-token-883 > /home/user/backup_op/restore_success.log`
   - Kill the background `storage_service` process using its PID.
   - Make sure your script is executable (`chmod +x`).

4. **Execute the Pipeline:**
   Run your `/home/user/backup_op/run_pipeline.sh` script. If successful, it will pull the mock backup data and populate `/home/user/backup_op/restore_success.log`.

Do not try to use `sudo` or modify system-wide user accounts. All actions should be contained within `/home/user/backup_op`.