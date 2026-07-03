You are an infrastructure monitoring specialist. We need to set up an automated network health check that runs automatically whenever configuration changes are committed to a local repository. 

A common pitfall with automated background tasks (like cron jobs or git hooks) is that they execute with different working directories or PATH variables than interactive shells, causing logs to be written to the wrong location (e.g., inside `.git/` instead of the project root). You must ensure your implementation uses absolute paths to avoid this issue.

Please complete the following tasks:

1. **Write a Network Health Check in C**:
   - Create a C program at `/home/user/check_port.c`.
   - The program should attempt a TCP connection to `127.0.0.1` on port `8080`.
   - If the connection succeeds, it must print exactly `STATUS: OK\n` to standard output.
   - If the connection fails, it must print exactly `STATUS: FAIL\n` to standard output.
   - Compile this program to an executable located at `/home/user/check_port`.

2. **Configure the Git Repository and Hook**:
   - Initialize a new git repository at `/home/user/monitor_repo`.
   - Create a `post-commit` hook in this repository (`/home/user/monitor_repo/.git/hooks/post-commit`).
   - The hook must execute `/home/user/check_port` and append its output to `/home/user/monitor_repo/net_log.txt`.
   - Next, the hook must implement a simple log rotation (backup): It should count the lines in `/home/user/monitor_repo/net_log.txt`. 
   - Once the file reaches exactly 3 lines, the hook must copy its contents to `/home/user/monitor_repo/net_log.bak` (overwriting any previous backup) and then completely empty `/home/user/monitor_repo/net_log.txt`.

Make sure your hook is executable. You do not need to start any services on port 8080; the automated verification will handle that during testing.