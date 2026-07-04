You are an infrastructure engineer automating the provisioning of a local telemetry monitoring system. We have a broken setup that was partially deployed. 

There is a wrapper script simulating a cron-like stripped environment, which is causing logs to write to the wrong location and fail to find network binaries due to `PATH` and `HOME` variable differences.

Your objectives are to fix the environment, extract network configuration data, and establish a proper log rotation policy.

**Step 1: Fix the Environment Wrapper**
There is a script at `/home/user/run_telemetry.sh` which simulates a scheduled task by overriding environment variables and then calling `/home/user/collect.sh`. 
Because `HOME` is incorrectly set to `/tmp` in the wrapper, `collect.sh` writes its output to `/tmp/logs/telemetry.log` instead of the required `/home/user/logs/telemetry.log`. Furthermore, it fails to execute network commands because `/sbin` and `/usr/sbin` are missing from the `PATH`.
- Fix `/home/user/run_telemetry.sh` by modifying it so `HOME` is explicitly set to `/home/user` and `PATH` includes `/sbin` and `/usr/sbin` (append or prepend them to the existing minimal PATH).
- **DO NOT** modify `/home/user/collect.sh`.
- Create the directory `/home/user/logs/` and execute `/home/user/run_telemetry.sh` so that it successfully generates `/home/user/logs/telemetry.log`.

**Step 2: Parse Network Configuration**
You will find a configuration file at `/home/user/net_config.ini` containing mock network interface settings.
- Write a bash script at `/home/user/extract_routes.sh` that reads `/home/user/net_config.ini`.
- For every section (e.g., `[eth0]`) that has a `gateway` defined, it should extract the interface name and the gateway IP.
- The script must write these to `/home/user/routes.txt` in the exact format: `interface:gateway_ip` (one per line, e.g., `eth0:192.168.1.1`).
- Execute your script to generate `/home/user/routes.txt`.

**Step 3: Log Configuration and Rotation**
- Create a `logrotate` configuration file at `/home/user/logrotate.conf` specifically for `/home/user/logs/telemetry.log`.
- The configuration must specify:
  - `daily` rotation.
  - Keep exactly `4` rotated logs (`rotate 4`).
  - `compress` the rotated logs.
  - `missingok`.
- Finally, create a dummy file at `/home/user/logs/telemetry.log` (if not already created by Step 1) and manually test the logrotate config by running: `logrotate -s /home/user/logrotate.state /home/user/logrotate.conf`. 

Ensure all files are located exactly where specified.