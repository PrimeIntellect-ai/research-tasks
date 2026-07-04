You are assisting a network engineer who is troubleshooting a local routing and connectivity issue. A temporary service has been set up on local port 8888, and we need an automated way to verify connectivity, parse current routing configurations, and log the results with a specific timezone.

Your task is to:

1. Write a C++ program at `/home/user/net_check.cpp`. This program must:
   - Create a TCP socket and attempt to connect to `127.0.0.1` on port `8888`.
   - If the connection is successful, print exactly the string `CONNECT_SUCCESS` to standard output.
   - If the connection fails, print exactly `CONNECT_FAIL` to standard output.
   - Ensure the program exits cleanly after the check.

2. Compile this C++ program to a binary located at `/home/user/net_check`.

3. Write a bash automation script at `/home/user/monitor.sh`. This script must:
   - Set the environment timezone to `America/New_York` for its execution scope.
   - Execute the `/home/user/net_check` binary and append its standard output to `/home/user/logs/net_status.log`.
   - Search the file `/home/user/routes.txt` for the line containing the exact string `default via`.
   - Append that exact matching line from `routes.txt` to `/home/user/logs/net_status.log`.

4. Make `/home/user/monitor.sh` executable and run it exactly once so that the log file is generated.

Do not hardcode the expected outputs in your log file. The C++ program and bash script must perform the actual connection test and file parsing.