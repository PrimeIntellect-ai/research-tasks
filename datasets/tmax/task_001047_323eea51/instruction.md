You are a DevOps engineer tasked with debugging a log aggregation script. 

There is a script located at `/home/user/aggregate_logs.sh`. This script is supposed to parse a server log file located at `/home/user/server_logs.txt`. 
The log file contains lines formatted like:
`YYYY-MM-DD HH:MM:SS [INFO] ResponseTime: <ms>`

The goal of the script is to calculate the average response time for each hour of the day. However, the server logs are in UTC, and the averages need to be reported in local time, which is UTC+3.

Currently, the script is broken. When run, it crashes with arithmetic and assertion errors. Upon inspecting the script and its standard error output, you will find two primary algorithmic/logic issues in how the script parses the hours and calculates the shifted timezone:
1. It fails to safely perform arithmetic on numbers with leading zeros (a classic Bash pitfall).
2. It fails to properly wrap the hour around midnight (i.e., adding 3 to 22 should result in hour 1, not 25, which currently trips a safety assertion in the script).

Your task:
1. Debug and modify `/home/user/aggregate_logs.sh` to fix the timezone formula implementation and the numeric parsing bugs using pure Bash.
2. Run the fixed script.
3. Ensure the script writes the correct aggregated results to `/home/user/hourly_averages.txt` exactly in the format: `Hour: <HH>, Avg: <ms>` (where HH is a zero-padded two-digit hour, e.g., `01`, `08`, `23`). The script already has a loop to output this, provided the data arrays are populated correctly without crashing.

Only use standard Bash built-ins and coreutils. Ensure the final output file is generated correctly at `/home/user/hourly_averages.txt`.