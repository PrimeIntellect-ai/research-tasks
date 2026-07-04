You are an edge computing engineer deploying software to resource-constrained IoT devices. You need to build a lightweight, custom process watchdog in C, along with a deployment and alert-processing pipeline using Bash. 

Your task consists of several phases:

**Phase 1: The C Watchdog**
Write a C program at `/home/user/watchdog.c` and compile it to `/home/user/watchdog`.
The program must:
1. Accept exactly two command-line arguments: the path to an executable to run, and the path to a log file. (e.g., `./watchdog /home/user/sensor_app /home/user/watchdog.log`)
2. Fork and execute the provided executable.
3. Wait for the child process to finish.
4. If the child process exits with a non-zero exit code or is terminated by a signal, the watchdog must append the exact string `[ALERT] Child crashed\n` to the log file.
5. The watchdog should restart the child process if it crashes.
6. The watchdog must give up and exit with code `1` after the child has crashed exactly 3 times. If the child exits cleanly (exit code 0), the watchdog should exit immediately with code `0`.

**Phase 2: Alert Mailer Script**
Write a Bash script at `/home/user/mailer.sh` that simulates an email alert system.
1. The script should read `/home/user/watchdog.log`.
2. For every line containing `[ALERT]`, it should create or append to a file at `/home/user/outbox/alerts.eml`.
3. The `.eml` file should contain the line: `Subject: Edge Device Alert - Process Restarted`.
4. Ensure the `/home/user/outbox` directory exists.

**Phase 3: CI/CD Deployment Script**
Write a deployment script at `/home/user/deploy.sh` that automates the setup. The script must:
1. Create the `/home/user/outbox` directory.
2. Set strict permissions on `/home/user/outbox` so that only the owner has read, write, and execute permissions (chmod 700).
3. Compile `/home/user/watchdog.c` to `/home/user/watchdog` using `gcc`.
4. Run the watchdog against a pre-existing dummy binary located at `/home/user/sensor_app`, outputting to `/home/user/watchdog.log`.
5. Run the `/home/user/mailer.sh` script after the watchdog finishes.

**Execution**
A crashing dummy application has been provided for you at `/home/user/sensor_app`. 
To complete the task, implement the required files and execute your `/home/user/deploy.sh` script so that the final state (logs, outbox, and emails) is generated on the system.