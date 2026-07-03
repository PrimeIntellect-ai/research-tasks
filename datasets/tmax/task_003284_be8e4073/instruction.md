You are a Site Reliability Engineer (SRE) responsible for monitoring the uptime of our global infrastructure. We have a daily data processing pipeline that takes raw ping logs, parses them into a structured JSON format using a C program, and then aggregates the total downtime across all regions using a Python script.

However, the pipeline is currently completely broken:
1. The C parser (`/home/user/uptime/log_parser.c`) fails to build. 
2. The Python aggregator (`/home/user/uptime/aggregator.py`) crashes with a recursion error when processing nested data.

Your task is to fix the pipeline and generate the final downtime summary.

Here is what you need to do:
1. Navigate to `/home/user/uptime`.
2. Diagnose and fix the build failure for the C program. You can modify `log_parser.c` or the `Makefile`. Ensure that running `make` successfully produces the executable `log_parser`.
3. Diagnose and fix the recursion issue in `aggregator.py`. The script is supposed to recursively sum up all integer values (downtime in minutes) embedded in a deeply nested JSON structure (which consists of dictionaries, lists, and integers). 
4. Once both are fixed, run the pipeline by feeding `/home/user/uptime/raw_logs.txt` into `log_parser`, and piping the output into `aggregator.py`.
5. Save the final output (a single integer representing the total downtime in minutes) to `/home/user/downtime_summary.txt`.

Ensure your fixes are robust and the final output file contains only the total integer value.