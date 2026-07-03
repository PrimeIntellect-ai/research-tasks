You are a monitoring specialist setting up an automated supervisor and alert system tied to source code deployments. 

Your objective is to create a local Git deployment pipeline that checks and supervises a critical background process whenever new code is pushed. Because our operations team is based in Japan, all alerts must be logged in the `Asia/Tokyo` timezone.

Perform the following steps in `/home/user`:

1. **The Target Service:**
   Create a dummy service script at `/home/user/app_service.sh` with the following content and make it executable:
   ```bash
   #!/bin/bash
   while true; do sleep 60; done
   ```

2. **The Git Repository:**
   Initialize a bare Git repository at `/home/user/service.git`.

3. **The Rust Supervisor:**
   Write a Rust program in a single file at `/home/user/monitor.rs` and compile it to `/home/user/monitor_bin` using `rustc`. 
   This Rust program must do the following:
   - Set the `TZ` environment variable to `Asia/Tokyo` for its process.
   - Execute the system `date` command with the format `+%Y-%m-%d %H:%M:%S %z` to get the current Tokyo time.
   - Check if the script `app_service.sh` is currently running (e.g., using `pgrep -f app_service.sh`).
   - If the service is **not running**, it must start it in the background (using `nohup /home/user/app_service.sh > /dev/null 2>&1 &` or equivalent so it outlives the Rust process) and append the following exact line to `/home/user/alert.log`:
     `[{TIME}] CRITICAL: Service was down. Restarted.`
   - If the service **is running**, it must append the following exact line to `/home/user/alert.log`:
     `[{TIME}] INFO: Deployment pushed. Service is active.`
   *(Replace `{TIME}` with the exact output obtained from the `date` command).*

4. **The Git Hook:**
   Create a `post-receive` hook inside `/home/user/service.git/hooks/post-receive`. Ensure it is executable. This hook should simply execute `/home/user/monitor_bin` whenever code is pushed to the repository.

Ensure all paths are absolute (`/home/user/...`) so the hook executes correctly regardless of the working directory Git uses. Do not start the service manually; the automated test will push to the repository to verify that your hook and Rust supervisor behave correctly in both the "down" and "active" states.