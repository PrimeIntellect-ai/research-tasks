You are an edge computing engineer deploying to remote IoT devices. These devices have highly constrained storage, and we need a lightweight bash-based health check to monitor telemetry data accumulation.

Your task is to implement a storage monitoring script and configure its environment.

Perform the following steps on the system:

1. **Environment Variable Setup**:
   Add an environment variable `MAX_STORAGE_MB` set to `40` to the end of the file `/home/user/.bashrc`. Ensure it is exported.

2. **Create the Monitoring Script**:
   Write a Bash script at `/home/user/monitor.sh`. The script must:
   - Be executable.
   - Source `/home/user/.bashrc` at the beginning to load the environment variables.
   - Calculate the total disk usage of the directory `/home/user/telemetry_data` in Megabytes. (Use `du -sm /home/user/telemetry_data` and extract the integer value).
   - Compare the directory size against the `MAX_STORAGE_MB` environment variable.
   - If the size is strictly greater than `MAX_STORAGE_MB`, append exactly this string to `/home/user/health.log`:
     `CRITICAL: Storage at <SIZE>MB exceeds limit of <MAX_STORAGE_MB>MB`
   - If the size is less than or equal to `MAX_STORAGE_MB`, append exactly this string to `/home/user/health.log`:
     `OK: Storage at <SIZE>MB within limit`

3. **Execution**:
   There is already some data in `/home/user/telemetry_data`. Execute your script `/home/user/monitor.sh` exactly once so that it evaluates the current directory size and writes the result to `/home/user/health.log`.

Pay close attention to the exact formatting of the log strings.