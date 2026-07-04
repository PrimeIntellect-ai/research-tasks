You are an observability engineer responsible for a local metrics gathering stack. Recently, our dashboard started showing missing data for "Service B", and the email alert system failed to notify the team. 

Your investigation reveals a misconfiguration in the network bindings and the alerting setup. You need to diagnose, backup, fix, and monitor the setup.

Please perform the following steps in the `/home/user/observability` directory:

1. **Backup Strategy**: Before making changes, copy the current configuration file `/home/user/observability/service_b.conf` to a new directory `/home/user/observability/backups/` and name the backup `service_b.conf.bak`.

2. **Connectivity & Process Control**: "Service B" is failing to start because it's bound to the wrong port in its configuration. 
   - Edit `/home/user/observability/service_b.conf` and change the `BIND_PORT` from `8083` to `8082` (the port the metrics gatherer expects).
   - Start the service by running the script `/home/user/observability/start_service_b.sh` in the background.

3. **Email Alert Configuration**: The alerting daemon failed because it was trying to reach a dead SMTP relay.
   - Edit `/home/user/observability/alert.conf` and change the `SMTP_PORT` variable from `2525` to the correct local relay port, `1025`.

4. **Scheduled Monitoring (Bash)**: We need a reliable way to ensure Service B stays reachable. 
   - Write a bash script at `/home/user/observability/monitor.sh` that uses `curl -s` to fetch `http://127.0.0.1:8082/metrics`. 
   - If the curl command succeeds (exit code 0), append the exact text `SERVICE_B_UP` to `/home/user/observability/dashboard.log`. If it fails, append `SERVICE_B_DOWN`.
   - Make the script executable.
   - Write the exact cron expression to run this script every minute as the user into a file named `/home/user/observability/cron_schedule.txt`. The file should contain exactly one line (the standard cron format, e.g., `* * * * * /home/user/observability/monitor.sh`).

Ensure all files are created with the exact paths and names specified.