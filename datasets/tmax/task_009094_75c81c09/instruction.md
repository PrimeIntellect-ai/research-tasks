You are an observability engineer tasked with tuning a simulated microservices logging environment. Your microservices are experiencing simulated network configuration issues, resulting in massive log spam. You need to implement log management, configuration tuning, and correct filesystem permissions so the mock CI/CD pipeline can read the logs.

Perform the following tasks in the `/home/user/obs/` directory (you will need to create it and its subdirectories: `logs/` and `config/`):

1. **Permission and ACL Management:**
   The CI/CD pipeline agent runs under the standard Linux `games` group. Configure the `/home/user/obs/logs/` directory using Access Control Lists (ACLs) so that the `games` group has default read (`r`) permissions for any *newly created* files within this directory. The directory itself must also allow the `games` group to read and execute (list) its contents.

2. **Interactive Configuration Script:**
   Create an interactive bash script at `/home/user/obs/tune.sh`. When executed, it must exactly prompt the user for the following in order:
   - `Service name: `
   - `Log level: `
   
   After receiving the inputs, the script should write a single line `LEVEL=<Log level>` to the file `/home/user/obs/config/<Service name>.env`. Ensure the script has executable permissions.

3. **Log Rotation Script:**
   Create a bash script at `/home/user/obs/log_rotator.sh` that checks all `.log` files in `/home/user/obs/logs/`. If a `.log` file is strictly greater than 100 bytes in size, the script should rotate it. The rotation policy is:
   - `<filename>.log` becomes `<filename>.log.1`
   - `<filename>.log.1` becomes `<filename>.log.2`
   - Any existing `<filename>.log.2` is overwritten/deleted.
   - The original `<filename>.log` should be emptied (truncated to 0 bytes).
   Make sure the script is executable.

4. **Service Lifecycle Management:**
   Create a systemd **user** service named `log-rotator.service` and an associated timer named `log-rotator.timer`.
   - The service should execute your `/home/user/obs/log_rotator.sh` script.
   - The timer should be configured to run the service periodically every 1 minute (`OnCalendar=*-*-* *:*:00` or `OnUnitActiveSec=1m`).
   - Enable and start the timer using `systemctl --user`.

Ensure all files are created with the exact paths and names specified. Do not require root/sudo access; use user-level systemd directories (`~/.config/systemd/user/`).