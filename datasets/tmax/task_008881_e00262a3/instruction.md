You are acting as a system administrator building a custom GitOps-style local operator in Go to manage mock application workloads.

Currently, there is a mock service running on the system. It consists of three background processes executing `/home/user/worker.sh` with arguments for their ID (1, 2, and 3) and their current version (`v1.0.0`). These workers constantly run and write initialization logs to `/home/user/logs/deploy.log`.

Your task is to write a Go program at `/home/user/deployer.go` that acts as a deployment operator to perform a staged rolling update of these processes and manage their log files. 

Your Go program must perform the following actions when executed:

1. **Read Manifest**: Parse the JSON file located at `/home/user/manifest.json`. It contains a single JSON object with a `target_version` string key (e.g., `{"target_version": "v2.1.0"}`).
2. **Log Rotation**: Before starting the deployment, check the size of `/home/user/logs/deploy.log`. If the file size is strictly greater than 100 bytes, rename it to `/home/user/logs/deploy.log.bak` (overwriting if it already exists).
3. **Rolling Staged Deployment**: 
   Iterate sequentially through worker IDs 1, 2, and 3. For each worker ID:
   - Identify the running process for that specific worker ID (e.g., the process running `bash /home/user/worker.sh 1 v1.0.0`).
   - Terminate the old process gracefully (SIGTERM).
   - Start a new background process using `/home/user/worker.sh <ID> <TARGET_VERSION>`. (The worker script internally appends its logs to `/home/user/logs/deploy.log`, so you do not need to capture its stdout in Go, just start the process).
   - Sleep for exactly 1 second before proceeding to the next worker ID to ensure a staged rollout.

**Environment Details:**
- The worker script is located at `/home/user/worker.sh`.
- The desired state manifest is at `/home/user/manifest.json`.
- Log directory is `/home/user/logs/`.
- Ensure your Go program is completely self-contained, compiles successfully, and is executed to apply the new target version specified in the manifest. You must compile and run your program to complete the task.