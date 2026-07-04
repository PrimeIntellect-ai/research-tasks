You are a deployment engineer tasked with fixing and automating a broken CI/CD pipeline. A recent update caused a configuration drift where some servers' SSH daemons silently reject key-based logins due to a missing signature algorithm configuration, causing the automated deployments to fail. 

Your objective is to build a set of Bash scripts that analyze the failure logs, set up a supervised local deployment service, establish a network tunnel, and orchestrate these steps into a CI/CD pipeline script.

All your work must be done in `/home/user`. You do not have root access.

**Step 1: Log Analysis (Text Processing)**
The deployment logs are located in `/home/user/logs/`. Each file is named `deploy_<id>.log`. 
Write a script named `/home/user/analyze.sh` that parses these logs to identify which servers rejected the SSH keys. 
* A failed login due to key rejection is indicated by a line containing exactly: `Connection closed by authenticating user deploy`
* For each file that contains this failure, extract the hostname and IP address from the line that looks like: `Connecting to host server-app-01 [192.168.1.15] port 22.`
* The script must output the extracted failed servers to `/home/user/failed_servers.txt` in the exact format: `<hostname>,<IP>` (e.g., `server-app-01,192.168.1.15`). Sort the output alphabetically by hostname.

**Step 2: Process Supervision**
There is a buggy deployment agent script at `/home/user/deploy_agent.sh` (already existing on the system). It often crashes.
Write a process supervisor script named `/home/user/supervisor.sh` that does the following:
1. Executes `/home/user/deploy_agent.sh`.
2. If the agent exits with a non-zero exit code, the supervisor must append the line `[WARN] Agent crashed, restarting` to `/home/user/supervisor.log` and restart the agent immediately.
3. If the agent crashes 3 times (i.e., fails on its 3rd execution), the supervisor should append `[ERROR] Max retries reached` to `/home/user/supervisor.log` and exit with code 1.
4. If the agent exits with code 0, the supervisor should append `[INFO] Agent succeeded` to `/home/user/supervisor.log` and exit with code 0.

**Step 3: Network Tunneling**
Write a script `/home/user/tunnel.sh` that sets up a local TCP port forward using `socat`.
* It must listen on local port `8080` and forward all traffic to `127.0.0.1:9090`.
* The script must start this forwarding in the background and write the PID of the `socat` process to `/home/user/tunnel.pid`.

**Step 4: The CI/CD Pipeline Orchestrator**
Write a master script `/home/user/pipeline.sh` that orchestrates the above steps:
1. Ensure the log file `/home/user/supervisor.log` is empty or created fresh.
2. Run `./analyze.sh`.
3. Run `./tunnel.sh`.
4. Run `./supervisor.sh`.
5. Upon completion of `supervisor.sh` (regardless of its exit code), read the `socat` PID from `/home/user/tunnel.pid` and terminate the tunnel process.
6. If `supervisor.sh` exits with code 0, write `PIPELINE SUCCESS` to `/home/user/pipeline_result.txt`. If it exits with a non-zero code, write `PIPELINE FAILURE` to `/home/user/pipeline_result.txt`.

Ensure all your scripts are executable. Run `/home/user/pipeline.sh` to complete the task.