You are managing user compute allocations on a centralized server. Users have configuration directories, remote assigned nodes, and assigned worker processes. You need to automate the detection of "Active" users and manage symbolic links to their directories for other system services to access.

Write a C++ program and a scheduling script to accomplish this.

Here are the requirements:
1. Create a C++ program located at `/home/user/account_monitor.cpp` and compile it to `/home/user/account_monitor`.
2. The C++ program must scan the directory `/home/user/managed_users/`. Each subdirectory represents a username.
3. For each user, read the contents of `/home/user/managed_users/<username>/node.txt`. This file contains a single IP address or hostname.
4. Determine if the user is "Active". A user is Active ONLY IF BOTH of the following are true:
   - The host in `node.txt` is reachable via a single ICMP echo request (e.g., `ping -c 1 -W 1 <host>` returns a successful exit code).
   - A process with the exact name `worker_<username>` is currently running on the system (you can use commands like `pgrep -x worker_<username>` to check).
5. Link Management:
   - If the user is Active, ensure a symbolic link exists at `/home/user/active_links/<username>` pointing exactly to their configuration directory `/home/user/managed_users/<username>`.
   - If the user is NOT Active, ensure no such symbolic link exists in `/home/user/active_links/` (remove it if it's there).
6. Logging: The C++ program must output its findings to `/home/user/monitor_log.txt`. Append to or overwrite the file, but by the end of execution, it must contain exactly one line per user in the format: `<username>:<STATUS>` where `<STATUS>` is either `ACTIVE` or `INACTIVE`. Sort the lines alphabetically by username.
7. Scheduling: Since we don't have root access for system-wide cron, write a bash script at `/home/user/schedule_monitor.sh` that acts as a custom daemon. It should run `/home/user/account_monitor`, sleep for 60 seconds, and repeat indefinitely. Start this script in the background.

Ensure the directories `/home/user/active_links/` exists before your C++ program attempts to create links in it. You may create it manually.

Once your background script is running and `/home/user/monitor_log.txt` correctly reflects the system state, your task is complete.