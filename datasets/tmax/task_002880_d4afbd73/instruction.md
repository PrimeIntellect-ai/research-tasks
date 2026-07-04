You are a network engineer troubleshooting connectivity issues in a legacy environment. You have discovered a mysterious, undocumented diagnostic daemon running on some nodes. You managed to extract the binary, which is located at `/app/netdiag_obfuscated`. 

Your goals are to understand what this binary does, replicate its behavior exactly in Python, and create an automated, idempotent deployment script for it.

Phase 1: Reverse Engineering & Replication
The binary `/app/netdiag_obfuscated` takes a single command-line argument (a string representing a custom network diagnostic payload) and prints a computed connectivity hash to standard output. 
Write a Python script located exactly at `/home/user/netdiag_replica.py` that takes the exact same command-line argument and produces the exact same standard output as the binary for any given input string.

Phase 2: Automated Deployment & Process Management
We need to treat this new Python script as a reliable service. 
Write a bash script at `/home/user/deploy_service.sh` that performs the following tasks idempotently (meaning it can be run multiple times without causing errors or duplicating configurations):
1. Creates a systemd user service file at `/home/user/.config/systemd/user/netdiag-replica.service`.
2. The service should be configured to execute `/usr/bin/python3 /home/user/netdiag_replica.py "DEFAULT_PAYLOAD"`.
3. The service must capture standard output to `/home/user/netdiag.log`.
4. The script must reload the systemd user daemon, enable the service to start on boot, and restart the service immediately.

Constraints:
- You do not have root access. All systemd interactions must use `systemctl --user`.
- Ensure `/home/user/.config/systemd/user/` exists before writing the service file.
- The Python script must exactly match the output of the stripped binary, character for character, for any alphanumeric input payload.