You are a capacity planner analyzing network and storage utilization for a reverse proxy load balancer. You have been provided with the proxy's routing configuration and access logs, but you need an automated way to process them because the legacy analysis tool you are writing requires interactive input.

Your task is to write a C++ program to aggregate the proxy logs based on the routing rules, and an `expect` script to automate its execution.

Step 1: Write the C++ Analyzer
Create a C++ program at `/home/user/analyzer.cpp` that does the following:
1. Reads a routing configuration file located at `/home/user/proxy_routes.conf`. Each line contains a frontend path and a backend IP address, separated by a space (e.g., `/api 192.168.1.10`).
2. Reads a reverse proxy log file located at `/home/user/proxy_access.log`. Each line contains a timestamp, a frontend path, and the number of bytes transferred, separated by spaces (e.g., `2023-10-01T12:00:00 /api 5042`).
3. Aggregates the total bytes transferred for each backend IP. (Map the paths from the log to the backend IPs using the routing configuration).
4. Prints exactly this prompt to standard output: `Enter capacity threshold (bytes): `
5. Reads an integer threshold from standard input.
6. Prints the backend IPs that have strictly exceeded the threshold, in the format: `Backend [IP] exceeded with [Bytes] bytes.` Each on a new line, sorted lexicographically by the IP address string.

Compile your program to `/home/user/analyzer`. Use `g++ -std=c++17 /home/user/analyzer.cpp -o /home/user/analyzer`.

Step 2: Write the Automation Script
Create an expect script at `/home/user/run_analysis.exp` that:
1. Spawns the `/home/user/analyzer` program.
2. Waits for the `Enter capacity threshold (bytes): ` prompt.
3. Sends the value `15000` followed by a newline.
4. Captures the output (the list of exceeded backends) and saves ONLY those "Backend..." lines into `/home/user/capacity_report.txt`. Ensure the prompt itself and any other expect artifacts are not in the final report file.

Both the compiled `/home/user/analyzer` and the `/home/user/run_analysis.exp` script must be present and fully functional.