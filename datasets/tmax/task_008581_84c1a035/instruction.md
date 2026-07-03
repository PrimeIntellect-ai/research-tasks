You are a deployment engineer rolling out updates for a lightweight internal service. The current deployment script at `/home/user/deploy.sh` is broken. It fails because it lacks proper environment variables, attempts to rotate logs from a directory that doesn't exist, and starts a mock web server without the required TLS certificates.

Your task is to fix the environment, implement the missing scripts for TLS and log rotation, and fix the deployment script so it executes everything in the correct dependency order.

Follow these steps exactly:

1. **Environment Variables Setup**:
   Append the following environment variables to `/home/user/.bash_profile`:
   - `APP_PORT=8443`
   - `APP_LOG_DIR=/home/user/app_logs`
   - `TLS_DIR=/home/user/tls`

2. **TLS Configuration Script**:
   Create a bash script at `/home/user/setup_tls.sh`. This script must:
   - Read the `TLS_DIR` environment variable.
   - Create the directory specified by `TLS_DIR` if it does not exist.
   - Use `openssl` to generate a self-signed RSA 2048-bit certificate (`server.crt`) and key (`server.key`) inside `$TLS_DIR`.
   - The certificate must be valid for exactly 30 days.
   - The Subject of the certificate must be exactly: `/C=US/ST=State/L=City/O=Company/CN=localhost`

3. **Log Rotation Script**:
   Create a bash script at `/home/user/rotate.sh`. This script must:
   - Check if the file `$APP_LOG_DIR/server.log` exists.
   - If it exists and its file size is strictly greater than 1000 bytes, copy it to `$APP_LOG_DIR/server.log.bak`.
   - Gzip the backup file to create `$APP_LOG_DIR/server.log.bak.gz` (overwrite if the gz file already exists).
   - Truncate (empty) the original `$APP_LOG_DIR/server.log` file to 0 bytes without changing its permissions or deleting it.

4. **Fix the Deployment Script**:
   Modify `/home/user/deploy.sh` so that it safely and correctly performs the following actions in this exact order:
   - Source `/home/user/.bash_profile` to load the variables.
   - Ensure the directory specified by `$APP_LOG_DIR` exists (create it if not).
   - Execute `/home/user/setup_tls.sh`.
   - Execute `/home/user/rotate.sh`.
   - Append the string "Starting server on port $APP_PORT with cert $TLS_DIR/server.crt" to `$APP_LOG_DIR/server.log`.

5. **Execution and Verification**:
   - Make sure all `.sh` scripts are executable.
   - Run `/home/user/deploy.sh`.
   - To test your log rotation, append 2000 bytes of random data to `/home/user/app_logs/server.log` (e.g., using `dd` or `head` from `/dev/urandom`), and then run `/home/user/deploy.sh` a second time.

Leave the final system state with the rotated log archive present in the log directory, and the new log file containing the final startup message.