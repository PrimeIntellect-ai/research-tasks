You are acting as a system reliability engineer. A custom background service running on this system is currently failing to start. 

The service consists of a Python email log processor located at `/home/user/app/daemon.py`, which is launched via `/home/user/app/run_service.sh`. The processor is designed to connect to an internal email metadata server, fetch recent logs, and process them. However, it crashes immediately upon execution.

Your task is to diagnose the failure, fix the environment/configuration, successfully run the service, and extract specific metrics from its output.

Here are your specific requirements:
1. **Diagnose and Fix the Environment**: `daemon.py` has strict localization and timezone requirements. It expects the timezone to be `Europe/Berlin` and the time locale (`LC_TIME`) to be explicitly set to `de_DE.UTF-8`. You must modify `/home/user/app/run_service.sh` to correctly export these environment variables before launching the Python script.
2. **Network Routing**: The `daemon.py` script attempts to connect to the email metadata server on `localhost:8080`. However, the actual server is running on `localhost:9090`. Since you cannot modify `daemon.py` (it is considered a read-only compiled artifact for this exercise), you must set up a local port forward so that traffic to local port 8080 is transparently routed to local port 9090. You can use SSH local port forwarding, `socat`, or standard bash networking tools.
3. **Execute**: Once the environment and network route are fixed, execute `/home/user/app/run_service.sh`. If successful, it will connect to the server, process the logs, and write the output to `/home/user/app/processed_logs.txt`.
4. **Log Processing**: Using bash text-processing tools (`awk`, `grep`, `sed`, etc.), parse `/home/user/app/processed_logs.txt`. You need to extract all email addresses that have a status of "550 Bounced". 
5. **Output**: Save the extracted bounced email addresses to `/home/user/bounced_emails.txt`. The file must contain exactly one email address per line, with no extra whitespace or text, and must be sorted alphabetically.

You have all the standard bash tools and Python 3 available. Note: Do not modify `/home/user/app/daemon.py`. You may only modify `/home/user/app/run_service.sh` and run commands in the terminal.