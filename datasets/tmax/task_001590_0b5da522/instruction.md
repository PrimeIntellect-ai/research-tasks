You are a Site Reliability Engineer (SRE) tasked with preparing a deployment package for monitoring a simulated Virtual Machine environment. The deployment involves network connectivity diagnostics, storage preparation, and log management. 

You do not have root privileges, so all configurations and files must be placed within your home directory (`/home/user`). A simulated VM service is already running locally on TCP port 8080.

Perform the following tasks:

1. **Connectivity Diagnostics (C Programming):**
   Write a C program at `/home/user/uptime_monitor.c` that checks the uptime of a local service.
   - It must accept a single command-line argument: the TCP port number to check on `127.0.0.1`.
   - It should attempt a TCP connection to that port.
   - If the connection succeeds, it must append the exact string `STATUS: OK\n` to the file `/home/user/vm_uptime.log`.
   - If the connection fails, it must append the exact string `STATUS: FAIL\n` to the same log file.
   - It should exit with code 0 on success, and 1 on failure.

2. **Automation Script:**
   Create a bash script at `/home/user/setup_env.sh` that automates the environment preparation. When executed, this script must perform the following actions:
   - **Compilation:** Compile `/home/user/uptime_monitor.c` to an executable named `/home/user/uptime_monitor` (using `gcc`).
   - **Storage Preparation:** Create a 10MB raw disk image at `/home/user/vm_data.img` (e.g., using `dd`) and format it as an `ext4` filesystem. (Note: format it directly, do not mount it).
   - **Fstab Configuration:** Generate a simulated fstab file at `/home/user/simulated_fstab` containing exactly one line to mount this image. Use the following parameters: device is `/home/user/vm_data.img`, mount point is `/mnt/vm_data`, filesystem type is `ext4`, options are `loop`, dump is `0`, and pass is `0`. Fields should be separated by spaces or tabs.
   - **Log Configuration:** Create a valid logrotate configuration file at `/home/user/vm_logrotate.conf` to manage `/home/user/vm_uptime.log`. It must specify: daily rotation, keep 4 rotated logs, compress old logs, and missingok.

3. **Execution:**
   - Make your bash script executable and run it.
   - Manually execute your compiled `/home/user/uptime_monitor` checking port `8080`.

Ensure all files match the exact names and paths requested.