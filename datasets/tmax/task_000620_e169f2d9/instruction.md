You are a network engineer troubleshooting connectivity issues for several internal microservices running on this system. Intermittent network drops have caused some services to hang, and a background diagnostic tool has logged these connection failures. 

Your task is to build an automated recovery pipeline that parses the diagnostic logs, identifies the failing services, terminates the hung processes, restarts them, and logs the recovery status idempotently.

You must create two files in `/home/user/`:

**Part 1: Log Parsing Script (`/home/user/analyze_logs.sh`)**
A diagnostic log is located at `/home/user/net_diag.log`. It contains noisy, unstructured network probe results. 
Write a bash script at `/home/user/analyze_logs.sh` that uses text processing tools (like `grep`, `awk`, or `sed`) to extract the unique port numbers of the services that have failed. 
- A failure is indicated by the words "FAILED" or "refused" (case-sensitive) on the same line as an IP:PORT pair. 
- The script should output ONLY the unique failed port numbers, one per line.

**Part 2: Automated Recovery Daemon (`/home/user/auto_recover.py`)**
Write a Python script at `/home/user/auto_recover.py` that performs the following actions:
1. Executes `/home/user/analyze_logs.sh` to retrieve the list of failed ports.
2. For each failed port, locate its current Process ID (PID). The PID for each service is stored in `/home/user/services/pids/<port>.pid`.
3. Kill the hung process associated with that PID.
4. Restart the service by calling the provided bash script: `/home/user/services/start_single.sh <port>`. This script will automatically spin up a new instance of the service in the background and overwrite the `.pid` file with the new PID.
5. Idempotently update a JSON configuration file at `/home/user/recovery_status.json`. 
   - If the file does not exist, create it.
   - If it exists, read and parse it so you can update it.
   - Add or update a key for each recovered port. The JSON structure must be exactly:
     `{ "<port_number>": {"status": "recovered", "new_pid": <the_new_pid_integer>} }`

Make sure `auto_recover.py` works even if run multiple times (it should update the JSON without duplicating entries or corrupting the file). Run your Python script to perform the recovery and generate the output JSON.