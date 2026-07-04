You are a capacity planner analyzing resource usage across multiple deployment zones. 

An interactive python tool has been provided to you at `/home/user/disk_reporter.py`. This tool analyzes directories and reports on files exceeding a certain size threshold. Since the tool is highly interactive, it prompts the user for several inputs via standard input:
1. "Enter directory path: "
2. "Enter size threshold in MB: "
3. "Output format (csv/json/text): "

Your task is to:
1. Create an `expect` script (or bash script utilizing `expect`) at `/home/user/run_analysis.sh` that automates interactions with `/home/user/disk_reporter.py`.
2. Query the disk reporter for two specific directories:
   - `/home/user/data/zoneA`
   - `/home/user/data/zoneB`
3. For both directories, use a size threshold of `10` (MB) and choose the `csv` output format.
4. Capture the output and write a bash command or script that parses these CSV results to calculate the total number of files across both zones that exceed the threshold, as well as the sum of their sizes in MB.
5. Save the final aggregated results in a file named `/home/user/capacity_summary.txt`. 

The `/home/user/capacity_summary.txt` file must have exactly the following format:
```
Total Files: <integer>
Total Size: <float> MB
```
(Note: Replace `<integer>` with the total count, and `<float>` with the exact sum of sizes in MB rounded to two decimal places, e.g., `82.00`).

Ensure your `/home/user/run_analysis.sh` is executable and cleanly automates the interactive prompts without manual intervention.