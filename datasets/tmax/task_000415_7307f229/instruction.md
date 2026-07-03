You are a network engineer troubleshooting connectivity across different staged environments. You need to deploy a new Go-based network monitoring tool to directories simulating mounted filesystems.

Your objective is to write a Go program (`/home/user/netmon.go`) and a Bash deployment script (`/home/user/deploy.sh`) to automate this process.

### 1. The Go Program (`/home/user/netmon.go`)
Write a Go program that acts as the network monitor. 
- It must accept exactly two command-line arguments: the path to a CSV file containing network connections, and the path to a passwd-style file.
  Example usage: `./netmon_v2 /home/user/conns.csv /home/user/mock_passwd`
- The connections CSV file has no header. Its columns are: `local_ip,remote_ip,status,uid`
- The passwd file uses the standard `/etc/passwd` format (colon-separated, user is column 1, uid is column 3).
- The program must parse both files, filter the network connections for those where the `status` is exactly `ESTABLISHED`, and map the `uid` from the connections file to the username in the passwd file. If a UID is not found in the passwd file, use the string `UNKNOWN`.
- For each `ESTABLISHED` connection, print exactly this format to Standard Output (one per line):
  `[<username>] <local_ip> <remote_ip>`
- Do not print anything else.

### 2. The Deployment Script (`/home/user/deploy.sh`)
Write a Bash script that performs a staged deployment of this Go program. The script must:
1. Compile `/home/user/netmon.go` to a binary named `netmon_v2` in `/home/user/`.
2. Terminate any currently running processes named exactly `netmon_v1`. (There are dummy legacy monitoring processes running in the background). Ensure they are successfully terminated.
3. Read the deployment configuration file located at `/home/user/deploy_fstab`. This file is formatted exactly like a standard Linux `/etc/fstab` (space/tab separated, ignore lines starting with `#`).
4. For every entry in `/home/user/deploy_fstab`, the 2nd column represents the `target_directory` (the mount point).
5. For each `target_directory` found:
   - Create the directory if it does not exist.
   - Copy the compiled `netmon_v2` binary into the `target_directory`.
   - Run the newly copied binary (`./netmon_v2`) using `/home/user/conns.csv` and `/home/user/mock_passwd` as its arguments.
   - Redirect the standard output of the binary to a file named `monitor.log` inside that `target_directory`.

### Execution
Once you have written both files, ensure `deploy.sh` is executable and run it to perform the deployment. The final verification will check that the `monitor.log` files are created in the correct directories with the exact expected mappings.