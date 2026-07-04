You are an operations specialist responsible for managing local CI/CD pipelines for a set of microservices. Your environment lacks root privileges, so all configurations must be handled within your home directory (`/home/user`).

Your objective is to implement a lightweight deployment orchestrator in Go, wire it up using Git hooks, configure the environment, and establish log rotation. 

Follow these steps exactly to configure the system:

1. **Environment Setup:**
   Create a profile file at `/home/user/.microservice_profile`. It must contain the following environment variable exports:
   - `DEPLOY_ENV=staging`
   - `TARGET_PORT=8080`
   - `LOG_DIR=/home/user/logs`

2. **The Go Orchestrator:**
   Create a Go source file at `/home/user/src/deployer.go`. The program must perform the following actions:
   - Read the environment variables `DEPLOY_ENV`, `TARGET_PORT`, and `LOG_DIR`. (Assume they are set by the caller).
   - Perform a TCP connection test to `127.0.0.1:9090` (a mocked dependency microservice). The timeout should be 2 seconds.
   - If the connection succeeds, append the exact string `[Timestamp] DEPLOYMENT SUCCESSFUL: Env=staging, Port=8080\n` to the file `$LOG_DIR/deploy.log`. (Replace `[Timestamp]` with the current time in RFC3339 format, and use the actual variables).
   - If the connection fails, append `[Timestamp] DEPLOYMENT FAILED: Dependency unreachable\n` to `$LOG_DIR/deploy.log` and exit with status code 1.
   Compile this program to `/home/user/bin/deployer`. Ensure the `bin` and `logs` directories exist.

3. **Git Server & Hook Configuration:**
   Initialize a bare Git repository at `/home/user/microservice.git`.
   Create a `post-receive` hook in this repository (`/home/user/microservice.git/hooks/post-receive`). The hook must:
   - Be executable.
   - Source the `/home/user/.microservice_profile` file.
   - Execute the compiled Go program: `/home/user/bin/deployer`.

4. **Log Rotation Configuration:**
   Create a local logrotate configuration file at `/home/user/logrotate.conf` for the log file `/home/user/logs/deploy.log`. Configure it to:
   - Rotate daily.
   - Keep exactly 3 backups.
   - Compress rotated files.
   - Missing log files should not cause an error (`missingok`).

To complete the task, push a dummy commit from a temporary local clone to `/home/user/microservice.git` to trigger the hook and generate the first log entry. Note: A mock service is already running on `127.0.0.1:9090` in the background.