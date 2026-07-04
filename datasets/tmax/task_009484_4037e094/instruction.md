You are a container specialist managing a fleet of microservices. Before a specific microservice container initializes, it must verify that its network-attached storage node is reachable. Because standard tools like `ping` or `nc` are stripped from the minimal container image, you must write a custom diagnostic tool in C++ and a robust shell script to drive the process.

Your task is to create two files:
1. A C++ program at `/home/user/tcp_checker.cpp`
2. A bash script at `/home/user/check_mount_conn.sh`

**Requirements for the C++ Program (`/home/user/tcp_checker.cpp`):**
- Must accept exactly two command-line arguments: `<ip>` and `<port>`.
- Must attempt to establish a standard TCP connection to the provided IP address and port using POSIX sockets.
- If the connection is successful, the program must exit with status code `0`.
- If the connection fails, the program must exit with status code `1`.

**Requirements for the Bash Script (`/home/user/check_mount_conn.sh`):**
- Must be a robust script that gracefully handles errors.
- First, check if the file `/home/user/config/micro_fstab` exists. If it does not exist, append exactly the string `ERROR: fstab missing` to `/home/user/mount_status.log` and exit with status `1`.
- If the file exists, parse it to find the entry for `storage_node`. The file follows a custom fstab format: 
  `<target_name> <ip> <port> <fstype> <options>`
- Extract the `<ip>` and `<port>` for the `storage_node` entry.
- Compile the C++ program to an executable named `/home/user/tcp_checker` (e.g., using `g++`).
- Execute the compiled `tcp_checker` passing the extracted IP and port.
- If the C++ program returns an exit code of `0`, append exactly `MOUNT_READY: storage_node at <ip>:<port>` to `/home/user/mount_status.log` and exit with status `0`.
- If the C++ program returns a non-zero exit code, append exactly `ERROR: Connection failed for storage_node` to `/home/user/mount_status.log` and exit with status `1`.

Make sure your shell script handles potential compilation errors or missing entries in the fstab gracefully.