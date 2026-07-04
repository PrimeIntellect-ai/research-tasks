You are an AI assistant helping a data scientist clean and analyze server metrics using pure Bash and standard Linux command-line tools (like `awk`, `join`, `sort`, etc.). No Python or other scripting languages are allowed.

You have two CSV files located in `/home/user/`:
1. `/home/user/cpu.csv` - Contains CPU metrics. Format: `timestamp,cpu_usage`
2. `/home/user/mem.csv` - Contains Memory metrics. Format: `timestamp,mem_usage`

The timestamps are integer Unix epochs. The files might not be perfectly sorted.

Your task is to write and execute bash commands to do the following:
1. **Join** the two files on the `timestamp` column so that only timestamps present in both files are kept.
2. **Sort** the joined dataset chronologically by timestamp (oldest to newest).
3. **Detect Anomalies** by scanning the sorted dataset. An anomaly is defined as a point in time where:
   - The CPU usage increased by **50 or more** compared to the *immediately preceding chronologically sorted row*.
   - AND the Memory usage at the *current* timestamp is **90 or more**.
   *(Note: The very first row in the sorted joined dataset cannot be an anomaly, as there is no preceding row to compare against).*
4. **Extract and Save** these anomalies to `/home/user/anomalies.csv`. The output format must be strictly: `timestamp,cpu_usage,mem_usage,cpu_increase` (no header row).

You must complete this task and create the `/home/user/anomalies.csv` file with the correct data.