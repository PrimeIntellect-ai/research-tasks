You are a Linux Systems Engineer handling an incident response. Our primary monitoring relay has failed, and we need to failover to a backup.

A few things are broken and need your attention. Complete the following objectives:

1. **Audio Alert Extraction**
   An automated voicemail alert was saved to `/app/outage_alert.wav`. Transcribe this audio file to retrieve the emergency backup SMTP port. Update the configuration file located at `/home/user/mailer.conf` to use this new port. The file should only contain the port number (e.g., `PORT=1234`).

2. **Systemd Service Dependency Fix**
   There is a user-level systemd service named `alert-sender.service` (located in `~/.config/systemd/user/`). It is currently failing to start. It crashes because it tries to write to a named pipe that is only created by `diagnostic-logger.service`. 
   Modify `alert-sender.service` so that it correctly waits for `diagnostic-logger.service` to start first. Enable and start both services successfully.

3. **Health Check Script Optimization**
   The script `/home/user/bin/check_endpoints.sh` performs connectivity diagnostics by verifying a list of 50 local endpoints. Currently, it runs these checks sequentially, which takes over 5 seconds.
   Your task is to refactor `/home/user/bin/check_endpoints.sh` using Bash to run the checks in parallel. 
   - The script must still output the exact same results to `/home/user/endpoint_status.log`.
   - The output format must remain unchanged (e.g., `Endpoint X: OK`).
   - The script must complete execution in under 0.5 seconds.
   
Ensure all services are running and `/home/user/bin/check_endpoints.sh` produces the correct output log within the time limit.