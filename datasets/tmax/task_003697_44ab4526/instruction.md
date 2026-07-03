I need you to act as a backup operator and set up a deployment script to test our legacy application restores. The restored database and app simulators have a network misconfiguration: the database binds to port 8081, but the app is hardcoded to look for the database on a port specified by the `DB_PORT` environment variable, and we need to proxy it through port 9091 to simulate our production load balancer. 

Write a bash script at `/home/user/deploy_restore_test.sh` that performs the following steps, and then execute it so the environment is fully running:

1. **SSH Tunneling (Load Balancer Simulation):** 
   Set up a background SSH local port forward mapping `127.0.0.1:9091` to `127.0.0.1:8081`. 
   *Note: Passwordless SSH to `127.0.0.1` for the current user is already configured.* 

2. **Environment Variable Setup:**
   Create a shell profile snippet at `/home/user/restore_env.sh` that exports two variables:
   - `DB_PORT=9091`
   - `RESTORE_ENV=testing`

3. **Service Lifecycle Management:**
   - Execute `/home/user/bin/db-restore.sh` in the background. 
   - Source the `/home/user/restore_env.sh` file, then execute `/home/user/bin/app-restore.sh` in the background.
   - Save the PIDs of both processes (the DB first, then the App, each on a new line) into a file located at `/home/user/service.pids`.
   - Also save the PID of the SSH tunnel process as the third line in `/home/user/service.pids`.

4. **Log Configuration and Rotation:**
   The services generate logs in `/home/user/logs/`. Create a logrotate configuration file at `/home/user/logrotate.conf` that targets `/home/user/logs/*.log` with the following rules:
   - Rotate when the file size reaches `10k`
   - Keep exactly `5` rotated backups
   - Compress the rotated files
   - Missing log files should not generate an error (`missingok`).
   
   At the end of your `deploy_restore_test.sh` script, trigger the log rotation manually once by running `logrotate` with your config file. Because you are not root, you must specify a custom state file located at `/home/user/logrotate.state`.

Make sure you run your script after creating it so that the final state of the system has the processes running, the tunnel active, and the logrotate configuration created and executed.