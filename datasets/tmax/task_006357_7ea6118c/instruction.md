You are tasked with managing a simulated microservice on a Linux server. The service sometimes crashes silently, leaving behind a stale PID file (similar to how some systems silently reject connections when in an inconsistent state).

The microservice executable is located at `/home/user/microservice.sh`. When started, it automatically writes its Process ID to `/home/user/service.pid` and listens for work.

Your task is to write a self-healing automation script and schedule it.

1. Create a bash script at `/home/user/ensure_service.sh` that does the following:
   - Checks if the PID file `/home/user/service.pid` exists.
   - If the PID file does NOT exist, start the service in the background using `nohup /home/user/microservice.sh > /home/user/service.log 2>&1 &`. Log the action.
   - If the PID file DOES exist, read the PID and check if the process is actually running.
   - If the process is running, take no action other than logging.
   - If the process is NOT running (the PID file is stale), remove the stale PID file and restart the service in the background as described above. Log the action.

2. The script must log its actions to `/home/user/watcher.log` by appending a single line per execution. The format MUST strictly be:
   `[YYYY-MM-DD HH:MM:SS] Action: <ACTION_TYPE>`
   Where `<ACTION_TYPE>` must be exactly one of: `STARTED`, `RUNNING`, or `RESTARTED` (corresponding to the three conditions above).
   Use `date "+%Y-%m-%d %H:%M:%S"` for the timestamp.

3. Schedule this script to run every minute using the user's `crontab`.

Ensure the script `/home/user/ensure_service.sh` has executable permissions.