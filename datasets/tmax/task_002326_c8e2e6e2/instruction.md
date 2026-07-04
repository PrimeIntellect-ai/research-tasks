You are a network engineer tasked with troubleshooting a failed staged deployment of an SSH tunnel mesh network. The central monitoring service crashed during the rollout, and connectivity is currently erratic. You must perform two critical recovery tasks: extract diagnostic data from a video recording of the monitor's dying moments, and implement a failover routing evaluator in Bash.

**Part 1: Diagnostic Extraction (Video)**
Before the monitoring console crashed, a screen recording was captured and saved to `/app/tunnel_monitor.mp4`. 
The video displays a scrolling log of connectivity checks. When a node's SSH tunnel completely failed, the log flashed a line containing the exact string `CRITICAL_DROP:` followed by an IP address (e.g., `CRITICAL_DROP: 10.20.30.40`).

1. Use tools like `ffmpeg` and `tesseract-ocr` (which you can install if needed) to parse the video.
2. Extract all unique IP addresses that experienced a `CRITICAL_DROP`.
3. Save the unique IPs, sorted in ascending numerical order (standard sort), one per line, to `/home/user/critical_nodes.txt`.

**Part 2: Failover Route Evaluator (Bash)**
To restore connectivity, we are moving to a localized script-based routing fallback. You must write a Bash script at `/home/user/route_filter.sh` that implements a Longest Prefix Match (LPM) routing table lookup.

The script must behave as follows:
- It takes exactly one argument: a target IPv4 address (e.g., `192.168.5.10`).
- It reads a routing table from Standard Input (`stdin`).
- Each line of the routing table contains a CIDR block and a Next Hop IP, separated by a space (e.g., `10.0.0.0/8 172.16.0.1`).
- The script must evaluate the target IP against all CIDR blocks in the table and find all matching routes.
- **Rule 1 (Longest Prefix Match):** The matching route with the largest subnet mask (longest prefix) wins. E.g., a `/24` match beats a `/16` match.
- **Rule 2 (Tie-breaker):** If multiple matching routes have the exact same prefix length (e.g., two overlapping `/24` networks somehow specified), the route that appears **first** (highest up) in the input routing table wins.
- **Rule 3 (Default):** If no routes match the target IP, the script must output exactly the word `DROP`.
- **Output:** The script must print *only* the Next Hop IP of the winning route (or `DROP`) to Standard Output, followed by a newline.

Example usage:
```bash
cat routes.txt | /bin/bash /home/user/route_filter.sh 10.10.5.5
```

Ensure your Bash script strictly follows standard IPv4 subnetting logic. Automated testing will intensely fuzz your script against thousands of random routing tables and IPs to verify its correctness.