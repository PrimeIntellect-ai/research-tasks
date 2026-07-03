You are a capacity planner responsible for analyzing the resource footprint of running virtual machines. A headless QEMU VM is currently running on your system, serving a VNC display on port 5900. 

Your objective is to build an automated, idempotent monitoring solution that logs the VM's connectivity and memory usage.

Task Instructions:

1. Create a Python script at `/home/user/poll_vm.py` that performs the following:
   - Diagnoses connectivity: Attempts a TCP connection to `127.0.0.1:5900` (the QEMU VNC port). Determine if the port is `UP` or `DOWN`.
   - Locates the running `qemu-system-x86_64` process and retrieves its Process ID (PID).
   - Reads the Resident Set Size (RSS) memory usage of this process in kilobytes (found as `VmRSS` in `/proc/<pid>/status`).
   - Appends a single line to `/home/user/vm_capacity.csv` with the exact format: `[YYYY-MM-DD HH:MM:SS],<VNC_STATUS>,<PID>,<RSS_KB>`
     (Example: `[2023-10-25 14:30:01],UP,10452,65432`)

2. Create a Bash script at `/home/user/deploy_job.sh` that securely and idempotently deploys this monitor:
   - It must ensure that `/home/user/vm_capacity.csv` exists. If the file is newly created, it must initialize it with the header: `TIMESTAMP,VNC_STATUS,PID,RSS_KB`
   - It must install a user cron job that executes `/usr/bin/python3 /home/user/poll_vm.py` every minute (`* * * * *`).
   - The script must be strictly **idempotent**. If `deploy_job.sh` is executed multiple times, it must not duplicate the cron job entry, and it must not overwrite or duplicate the CSV header if the file already exists.

3. Execution:
   - Make your scripts executable.
   - Run `/home/user/deploy_job.sh` to configure the system.
   - Manually execute `/home/user/poll_vm.py` exactly once so that at least one data entry is present in the CSV file for immediate analysis.