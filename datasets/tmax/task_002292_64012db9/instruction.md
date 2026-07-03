You are a Site Reliability Engineer (SRE) tasked with building a local uptime and storage monitoring tool, complete with a basic CI/CD deployment script. 

The system has service configurations stored in `/home/user/services-available/`.
Your task consists of the following steps:

1. **Directory and Link Management:**
   Create a directory named `/home/user/services-enabled/`. 
   Create symbolic links in this directory pointing to `/home/user/services-available/web.json` and `/home/user/services-available/api.json` (do not link any other services that might be in the available directory).

2. **Monitoring Script (`/home/user/monitor.py`):**
   Write a Python script that performs the following:
   - Iterates through all `.json` files in `/home/user/services-enabled/`. Each JSON file contains a `name` and a `port` key.
   - For each service, attempts to establish a brief TCP connection to `127.0.0.1` on the specified `port` with a 1-second timeout.
   - Calculates the storage usage of the `/home` partition. The disk usage percentage should be calculated as `int((used / total) * 100)`.
   - Generates a report line for each service and appends it to `/home/user/report.txt`. 
   
   **Log Format Requirements:**
   The timestamps must strictly be evaluated in the `Asia/Tokyo` timezone, displaying `JST` as the timezone abbreviation. 
   Format each line exactly as follows:
   `[YYYY-MM-DD HH:MM:SS JST] Service <name> on port <port> is <UP/DOWN>. Home disk usage: <X>%`
   *(Replace `<name>`, `<port>`, `<UP/DOWN>`, and `<X>` with the evaluated values. UP means the TCP connection was successful, DOWN means it failed/timed out).*

3. **CI/CD Pipeline Construction (`/home/user/pipeline.sh`):**
   Write a bash script at `/home/user/pipeline.sh` that simulates a CI/CD pipeline:
   - It must first check the syntax of your Python script using `python3 -m py_compile /home/user/monitor.py`.
   - If the syntax check fails, the bash script should exit with a non-zero status code.
   - If the syntax check passes, it should create the directory `/home/user/bin/` (if it doesn't exist) and create a symbolic link `/home/user/bin/monitor` pointing to `/home/user/monitor.py`. Make sure the Python script is executable.

After completing the scripts, run `/home/user/pipeline.sh` successfully, and then execute `/home/user/bin/monitor` once to generate the initial `/home/user/report.txt`.