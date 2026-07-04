You are a FinOps analyst tasked with optimizing and monitoring cloud costs. We need a local monitoring daemon that calculates daily costs from a billing export and sends an email alert if a threshold is exceeded. 

Your task is to implement the monitoring tool in C++, set up a user-space port forward to route traffic to our local mailing list server, and create a supervisor script to ensure the monitor stays running even if it encounters a bad record and crashes.

Perform the following steps:

1. **Write the Monitor Code**: Create a C++ program at `/home/user/finops_alert.cpp`.
   - It should continuously read from `/home/user/usage.csv` once every 2 seconds.
   - The CSV format has no header and contains: `InstanceID,HoursUsed,HourlyRate` (e.g., `i-0abcd,24,1.50`).
   - Calculate the total cost (sum of `HoursUsed * HourlyRate` across all lines).
   - If the total cost is strictly greater than `1000.00`, it must connect to a local SMTP proxy on `127.0.0.1` port `2525` and send an alert email.
   - The email must follow this exact SMTP sequence (ending lines with `\r\n` as per SMTP standards):
     ```
     HELO finops
     MAIL FROM:<finops@local>
     RCPT TO:<alerts@local>
     DATA
     Subject: Cost Alert
     Total cost is $<TOTAL_COST>
     .
     QUIT
     ```
     *(Format `<TOTAL_COST>` to exactly 2 decimal places).*
   - **Crash simulation:** If the program reads an `InstanceID` exactly equal to `CRASH_TEST`, it must immediately exit with status code `1` (simulating a fatal parsing error).

2. **Network Forwarding**: Our local test mailing list server actually listens on port `8025` (already running via a provided script `/home/user/mock_smtp.py`). Because legacy systems mandate using port `2525`, your C++ program must connect to `2525`. You must set up a port forward mapping TCP `127.0.0.1:2525` to `127.0.0.1:8025` using `socat`.

3. **Process Supervision**: Write a bash script `/home/user/supervisor.sh`.
   - This script should compile `/home/user/finops_alert.cpp` to `/home/user/finops_alert`.
   - It should then run `/home/user/finops_alert` in a supervision loop.
   - If `/home/user/finops_alert` exits with a non-zero exit code (crashes), the supervisor must restart it immediately.
   - If it exits with a `0` exit code, the supervisor should break the loop and exit.

4. **Startup**: Create a master script `/home/user/start_all.sh` that:
   - Starts the `socat` port forward in the background.
   - Starts `/home/user/mock_smtp.py` in the background (this script exists).
   - Starts `/home/user/supervisor.sh` in the background.
   - Exits with `0`.

Once you have written all the files, run `/home/user/start_all.sh` to begin the processes. Do not write anything to `usage.csv` yourself; the automated tests will populate it to verify your system's behavior.