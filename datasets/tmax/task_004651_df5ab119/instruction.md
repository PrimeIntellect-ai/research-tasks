You are a container specialist responsible for setting up a custom, lightweight microservice stack for a local unprivileged user. Since you do not have root access, everything must be configured using user-space tools and local directories.

Your task is to implement a simple C microservice, configure it to run as a user-level systemd service, and write an idempotent script to manage its logs.

Perform the following steps exactly as specified:

1. Create the necessary directories: `/home/user/src`, `/home/user/bin`, `/home/user/logs`, `/home/user/scripts`, `/home/user/config`, and `/home/user/.config/systemd/user`.

2. Write a C program at `/home/user/src/microservice.c`.
   - The program should run in an infinite loop.
   - Once every second, it must append the string "SERVICE_OK\n" to `/home/user/logs/micro.log`.
   - Make sure it flushes the output so it appears immediately.
   - Compile this program into an executable located at `/home/user/bin/microservice`.

3. Create a user systemd service file at `/home/user/.config/systemd/user/micro.service`.
   - The service description should be "Microservice Daemon".
   - The ExecStart should point to `/home/user/bin/microservice`.
   - Set `Restart=always`.
   - Once created, reload the user daemon, and start the service using `systemctl --user start micro.service`. (Do not worry if systemctl fails due to container environment limitations during execution, but you must execute the start command and ensure the unit file is perfectly formatted).

4. Write an idempotent shell script at `/home/user/scripts/setup_logrotate.sh`.
   - When executed, this script must generate a logrotate configuration file at `/home/user/config/micro-logrotate.conf`.
   - The generated configuration should target `/home/user/logs/micro.log`.
   - It must specify the following rules: `hourly`, keep `5` rotations (`rotate 5`), `missingok`, `compress`, and `copytruncate`.
   - The script must be idempotent: running it multiple times should result in the exact same `/home/user/config/micro-logrotate.conf` file (e.g., safely overwrite it or check if it exists).
   - Ensure `/home/user/scripts/setup_logrotate.sh` is executable and run it once.