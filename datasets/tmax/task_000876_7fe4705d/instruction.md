You are a system administrator maintaining custom network security tools. We have a legacy access control check that needs to be rewritten in C++ and deployed with proper configuration, logging, and diagnostics.

Please complete the following tasks:

1. **C++ IP Filter Utility**:
   Write a C++ program at `/home/user/src/ip_filter.cpp` that takes exactly one command-line argument: an IP address.
   - The program must read the Access Control List (ACL) from `/home/user/config/acl.conf`.
   - Each line in `acl.conf` contains one permitted IP address.
   - If the provided IP address matches a line in the ACL file exactly, the program must:
     a) Append the string `[ALLOW] <IP>` followed by a newline to `/home/user/logs/filter.log`.
     b) Exit with status code `0`.
   - If the IP address does NOT match any line (or if the ACL file is empty/missing), it must:
     a) Append the string `[DENY] <IP>` followed by a newline to `/home/user/logs/filter.log`.
     b) Exit with status code `1`.
   Compile this program to the executable `/home/user/bin/ip_filter` (you may use `g++`).

2. **Idempotent Setup & Permissions**:
   Write a bash script at `/home/user/setup_env.sh` that sets up the environment. When executed, it must:
   - Create the directories `/home/user/src`, `/home/user/bin`, `/home/user/config`, and `/home/user/logs` if they do not exist.
   - Create the file `/home/user/config/acl.conf` containing exactly two lines: `10.0.0.5` and `192.168.1.100`. If the file already exists, it should ensure these are the only contents.
   - Set the permissions of `/home/user/config/acl.conf` to exactly `400` (read-only for the owner, no permissions for group/others).
   - Create an empty `/home/user/logs/filter.log` if it does not exist, with permissions `644`.
   This script must be entirely idempotent (safe to run multiple times without errors or unintended changes).

3. **Log Rotation**:
   Write a bash script at `/home/user/rotate.sh` that implements a simple log rotation for `/home/user/logs/filter.log`.
   - It should keep a maximum of 3 old log files (`filter.log.1`, `filter.log.2`, `filter.log.3`).
   - When run, it shifts existing logs: `.2` becomes `.3` (overwriting any existing `.3`), `.1` becomes `.2`, and the current `filter.log` becomes `filter.log.1`.
   - Finally, it must create a fresh, empty `filter.log` with `644` permissions.

4. **Connectivity Diagnostics**:
   Write a bash script at `/home/user/test_filter.sh` that verifies the C++ utility. It must:
   - Call `/home/user/bin/ip_filter 10.0.0.5`.
   - Call `/home/user/bin/ip_filter 10.0.0.99`.
   - If the first command succeeds (exit 0) AND the second fails (exit 1), append `DIAGNOSTICS_PASSED` to `/home/user/logs/diagnostics.txt`.

Execute your setup script, compile your code, and run the diagnostics script before finishing.