You are an edge computing engineer deploying software to an IoT gateway device. You need to automate the execution, monitoring, and log management of a legacy sensor daemon that unfortunately requires interactive configuration on startup.

The legacy binary is located at `/home/user/legacy_sensor_bin`. 
When executed, it prompts the user exactly as follows:
1. `Device Name? `
2. `Mode? `

Your task is to implement the following automated deployment:

1. **Expect Script:**
   Write an `expect` script at `/home/user/launcher.exp` that spawns `/home/user/legacy_sensor_bin`. 
   - It must answer the `Device Name? ` prompt with `edge-node-01`.
   - It must answer the `Mode? ` prompt with `telemetry`.
   - The expect script must log all output from the spawned process to `/home/user/telemetry.log` (you can handle this via Expect's `log_file` command or by redirecting the output of the Expect script).
   - The script must keep the spawned process running indefinitely.

2. **Watchdog Script:**
   Write a Bash script at `/home/user/watchdog.sh` (ensure it is executable). 
   - When executed, it must check if the `legacy_sensor_bin` process is currently running.
   - If it is not running, the watchdog must start your `launcher.exp` script in the background (detached from the terminal) so the sensor binary continues running after the watchdog script exits.
   - If it is already running, it should do nothing and exit gracefully.

3. **Log Rotation:**
   Create a local logrotate configuration file at `/home/user/rotate.conf` to manage `/home/user/telemetry.log`.
   Configure it with the following rules:
   - Rotate the log file if its size exceeds `100 bytes` (so we can test it quickly).
   - Keep exactly `2` old rotated backups.
   - Do NOT compress the logs.
   - Create a new, empty log file after rotation.

4. **Execution and Testing:**
   - Execute your `/home/user/watchdog.sh` to start the sensor daemon in the background.
   - Wait a few seconds for `/home/user/telemetry.log` to accumulate more than 100 bytes of data.
   - Manually trigger your logrotate configuration exactly once by running:
     `logrotate -s /home/user/lr.state /home/user/rotate.conf`

Once complete, the legacy binary should be actively running in the background, your `telemetry.log` should have been rotated (creating a `.1` file), and a fresh `telemetry.log` should be actively receiving new data.