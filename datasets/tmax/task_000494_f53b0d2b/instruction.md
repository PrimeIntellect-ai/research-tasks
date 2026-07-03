You are a network engineer troubleshooting connectivity for custom file mounts. Your team relies on a custom fstab file for tracking network shares, but intermittent DNS and connectivity issues are causing silent failures.

Your task is to create a monitoring system consisting of a C++ program and a robust Bash wrapper script.

1. Write a C++ program located at `/home/user/nfs_monitor.cpp`.
   - The program must accept a file path as a command-line argument. This file represents a custom fstab format (e.g., `host:/remote/path /local/path nfs defaults 0 0`).
   - Read the file line by line. Ignore empty lines or lines starting with `#`.
   - For each valid line, extract the hostname (the substring before the first `:`).
   - Use the C/C++ `getaddrinfo` function to attempt DNS resolution for the extracted hostname.
   - If the hostname fails to resolve, generate an email payload in the directory `/home/user/outbox/`. The file must be named exactly `alert_<hostname>.txt`.
   - The contents of the alert file must be exactly:
     ```
     To: netops@domain.local
     From: monitor@domain.local
     Subject: Unreachable NFS Host: <hostname>

     Error: <hostname> failed DNS resolution.
     ```

2. Write a robust Bash script located at `/home/user/check_mounts.sh`.
   - The script must use `set -e` to handle errors.
   - It should compile the C++ program to `/home/user/nfs_monitor` using `g++`.
   - Ensure the directory `/home/user/outbox/` exists (create it if it doesn't).
   - Verify that the file `/home/user/custom_fstab` exists. If not, exit with status code 1.
   - Execute the compiled `nfs_monitor` binary, passing `/home/user/custom_fstab` as the argument.

To test your solution, you should create `/home/user/custom_fstab` with the following contents before running your script:
```
# This is a test fstab
localhost:/var/nfs /mnt/nfs nfs defaults 0 0
broken-server.invalid:/backup /mnt/backup nfs ro 0 0
127.0.0.1:/data /mnt/data nfs rw 0 0
unreachable-node.localdomain.invalid:/logs /mnt/logs nfs defaults 0 0
```
Run your bash script so that the necessary output files are generated for verification.