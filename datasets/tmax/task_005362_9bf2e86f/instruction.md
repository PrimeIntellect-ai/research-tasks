You are an infrastructure engineer tasked with automating the provisioning and process supervision of a legacy application.

There is an interactive installer script located at `/home/user/app-installer.sh`. You need to fully automate its installation and then write a custom supervisor to enforce storage quotas on it.

Perform the following steps:

1. **Automate the Installation (Expect Script)**
   Write an Expect script at `/home/user/provision.exp` that executes `/home/user/app-installer.sh`. The installer will prompt for three configuration values interactively. Your script must provide the following responses exactly:
   - Prompt: `Enter instance name: ` -> Send: `prod-worker`
   - Prompt: `Enter port number: ` -> Send: `9090`
   - Prompt: `Enable verbose mode? (y/n): ` -> Send: `y`
   
   Run your Expect script to complete the installation. A successful installation will automatically generate a service executable at `/home/user/service.sh` and a data directory at `/home/user/volume/`.

2. **Create a Supervisor with Quota Monitoring (Bash)**
   The newly installed `/home/user/service.sh` acts like a poorly-behaved containerized application: it runs continuously and rapidly fills up its data directory (`/home/user/volume/`). Since we lack standard container quotas, you must write a Bash script at `/home/user/supervisor.sh` to supervise it.

   Your supervisor script must do the following in a continuous loop:
   - Start `/home/user/service.sh` in the background.
   - Every 1 second, check the total size of `/home/user/volume/` in kilobytes (using `du -sk`).
   - If the size strictly exceeds 50 KB:
     1. Terminate the running `service.sh` process.
     2. Delete all contents inside `/home/user/volume/` (i.e., `rm -rf /home/user/volume/*`).
     3. Append exactly this line to `/home/user/supervisor.log`:
        `[QUOTA ENFORCED] Restarted prod-worker`
     4. Start `/home/user/service.sh` in the background again and resume monitoring.

3. **Execution**
   Run your `supervisor.sh` script until exactly 3 quota enforcement events have been logged in `/home/user/supervisor.log`. Once there are 3 lines in the log, you may manually terminate your supervisor script (or program your script to exit automatically after the 3rd restart).

Ensure the log file `/home/user/supervisor.log` contains exactly 3 lines with the specified string.