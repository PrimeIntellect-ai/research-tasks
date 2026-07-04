You are a container specialist managing a cluster of microservices. Several storage-backed microservices have lost connectivity to their data volumes and the service registry. Your task is to diagnose the failing endpoints, automate data retrieval from an interactive registry console, and prepare a mock filesystem configuration for the container runtime.

Complete the following steps:

1. **Automate Interactive CLI (Expect Scripting):**
   There is a mock service registry console located at `/home/user/registry_cli.py`. It requires interactive authentication. 
   Write a Python script at `/home/user/get_endpoints.py` that uses the `pexpect` library to interact with `/home/user/registry_cli.py`. 
   - When prompted for `Username:`, send `admin`.
   - When prompted for `Password:`, send `micro_pass_42`.
   - When prompted with `registry> `, send the command `get-failing-nodes`.
   - Capture the output of this command, which will be a list of IP addresses.
   - When prompted with `registry> ` again, send `exit`.
   - Your Python script must save *only* the IP addresses extracted from the output, one per line, into `/home/user/failing_ips.txt`.

2. **Log Processing Pipeline:**
   A network traffic log is located at `/home/user/network.log`. 
   Using bash text processing tools (e.g., awk, sed, grep), find all log entries in `/home/user/network.log` that correspond to the IPs in `/home/user/failing_ips.txt`. 
   Extract the unique error codes (e.g., `ERR-503`, `ERR-TIMEOUT`) associated with these IPs.
   Save the unique error codes, sorted alphabetically, one per line, into `/home/user/failing_errors.txt`.

3. **Filesystem Configuration (fstab):**
   The failing containers need their data volumes re-mapped via the container runtime's custom fstab file.
   Create a file at `/home/user/container_fstab`.
   Add exactly one line to this file to simulate a bind mount. It must map the source directory `/home/user/shared_data` to the target directory `/mnt/service_data` using the `bind` filesystem type. The mount options must be `ro,nosuid` and the dump/pass values must be `0 0`.
   Format it exactly like a standard `/etc/fstab` line (space or tab separated).

4. **Connectivity Diagnostics Code:**
   Write a Python script at `/home/user/diagnose.py` that reads `/home/user/failing_ips.txt`. For each IP, the script should simulate a ping by creating a JSON file at `/home/user/diag_report.json` with the following structure:
   ```json
   {
       "192.168.1.10": "unreachable",
       "192.168.1.15": "unreachable"
   }
   ```
   (Map every IP found in the text file to the string "unreachable").

Ensure all requested files are created at their exact specified paths with the exact requested contents.