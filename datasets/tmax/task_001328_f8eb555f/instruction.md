You are a backup operator automating the testing of server restores. Since you are testing this in a restricted user environment, you cannot use root commands directly. Instead, you need to write a Python script that parses backup configuration files, generates simulation scripts, and runs a custom process supervisor to test a restored application.

Write a Python script at `/home/user/test_restore.py` that performs the following three tasks:

1. **Mount Configuration Parsing**:
   Read the simulated fstab file located at `/home/user/backup/fstab.txt`. Extract the absolute paths of all mount points that have the filesystem type `nfs`. Write these mount points, one per line, sorted alphabetically, to `/home/user/nfs_mounts.log`.

2. **Firewall Rule Generation**:
   Read the network backup file located at `/home/user/backup/firewall.json`. This file contains a JSON object with a key `"blocked_ips"` pointing to a list of IP addresses. Generate a shell script at `/home/user/iptables.sh` that contains the necessary `iptables` commands to block inbound traffic from each of these IPs. The commands should follow the format: `iptables -A INPUT -s <ip_address> -j DROP`. Write one command per line, in the same order as they appear in the JSON file. Ensure the generated shell script has a `#!/bin/bash` shebang at the top.

3. **Process Supervision**:
   A restored application script is located at `/home/user/backup/flaky_app.sh`. Your Python script must act as a basic process supervisor. It should execute `/home/user/backup/flaky_app.sh` as a subprocess. If the script exits with a non-zero exit code, your Python script must immediately restart it. It should attempt a maximum of 3 restarts (i.e., a total of 4 executions). 
   Every time the subprocess crashes (non-zero exit), append a line to `/home/user/app_restarts.log` in the exact format: `Crash detected. Exit code: <code_here>`. 
   If the subprocess exits with code `0` or if the maximum number of restarts is reached, the supervisor should stop and your Python script should terminate cleanly.

Run your `/home/user/test_restore.py` script so that all output files are generated.