You are managing a lightweight, custom Kubernetes-like operator. Your task is to implement the operator logic in Python and a process supervisor in Bash.

1. Write a Python script at `/home/user/operator.py` that performs the following system checks:
   - **Routing Diagnostics**: Find the default gateway IP address by parsing the output of the `ip route` command. If no default gateway exists, use `127.0.0.1`.
   - **Connectivity Diagnostics**: Ping the identified IP address with a single packet. Record the result as `SUCCESS` if the ping command succeeds (exit code 0), and `FAILURE` otherwise.
   - **Storage Monitoring**: Calculate the total disk usage of the directory `/home/user/storage_dir` in kilobytes (KB). Round up to the nearest integer if necessary.
   - **Manifest Parsing**: Read the JSON file at `/home/user/manifest.json` and extract the integer value of `max_storage_kb`.
   - **Status Evaluation**: Determine the overall health. The status is `HEALTHY` if the ping result is `SUCCESS` AND the disk usage is less than or equal to `max_storage_kb`. Otherwise, the status is `UNHEALTHY`.
   - **Logging**: Append a single line to `/home/user/operator.log` in this exact format:
     `GW: <IP> | PING: <SUCCESS|FAILURE> | STORAGE: <KB> KB | STATUS: <HEALTHY|UNHEALTHY>`

2. Write a Bash script at `/home/user/supervisor.sh` that acts as a simple process supervisor:
   - It must execute `python3 /home/user/operator.py` exactly 3 times.
   - It must pause for exactly 1 second between each execution.

3. Once you have created both scripts, execute `/home/user/supervisor.sh` so that `/home/user/operator.log` is populated with exactly 3 lines of output.