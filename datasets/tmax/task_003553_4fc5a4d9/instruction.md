I am trying to configure a local health check system using systemd user units to monitor a dummy local service, but it is currently failing. I wrote a Bash script to do the check, but it crashes, fails to connect, and doesn't log correctly. 

Please resolve the issues by completing the following steps:

1. **Fix the Health Check Script**: 
   I have a script located at `/home/user/scripts/health_check.sh`. It is supposed to send an HTTP GET request to `http://127.0.0.1:8080/ping`. 
   - Fix any typos or bugs in the script (there are a couple).
   - Ensure the script creates the log directory `/home/user/logs` if it doesn't exist.
   - On a successful HTTP 200 response, it must append the exact string `STATUS: OK` to `/home/user/logs/health.log`.
   - Run the script once manually to verify it works and generates the log entry. (A dummy python web server is already running on port 8080 in the background).

2. **Configure the Scheduled Task**:
   Create the systemd user service and timer files to run this script automatically. Since you don't have root access, place them in `/home/user/.config/systemd/user/`.
   - Create a service file named `health-check.service` that executes `/home/user/scripts/health_check.sh`.
   - Create a timer file named `health-check.timer` that triggers this service every 5 minutes (using an `OnCalendar` expression for every 5 minutes).

Do not worry about enabling or starting the systemd timer using `systemctl`, as the systemd daemon might not be fully active in this container environment. Just ensure the unit files are perfectly formatted and located in the correct directory.