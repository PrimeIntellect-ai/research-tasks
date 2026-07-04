You are an infrastructure engineer automating a provisioning verification step. Your goal is to write a short health-check script that cleans up storage, switches the active environment configuration via symlinks, and performs connectivity diagnostics.

Perform the following tasks:

1. **Storage Cleanup & Directory Management**: 
   The directory `/home/user/provisioning/logs/` contains old log files taking up quota. Delete all files ending with `.old` in this directory.

2. **Configuration Management**: 
   There are environment-specific configuration files in `/home/user/provisioning/configs/`. Create a symbolic link at `/home/user/provisioning/active.conf` that points to `/home/user/provisioning/configs/prod.conf`.

3. **Connectivity Diagnostics Script**:
   Create a bash script at `/home/user/provisioning/run_check.sh` that does the following:
   - First, checks if the number of files in `/home/user/provisioning/logs/` is greater than 5. If it is, print "Storage quota exceeded" to standard output and exit with code 1.
   - Reads the active configuration file (`/home/user/provisioning/active.conf`). Each line in this file contains a hostname and a port, separated by a space (e.g., `google.com 443`). Ignore empty lines.
   - For each endpoint, uses `nc` (netcat) with a 2-second timeout (`-w 2`) and zero-I/O mode (`-z`) to verify TCP connectivity to that host and port.
   - Appends the result to `/home/user/provisioning/logs/connectivity.log`. 
     - If the connection succeeds, append: `SUCCESS: <hostname>:<port>`
     - If the connection fails, append: `FAILURE: <hostname>:<port>`

4. **Execution**:
   Make your script executable and run it. 

Ensure the final `connectivity.log` file is formatted exactly as specified, as automated systems will parse this file.