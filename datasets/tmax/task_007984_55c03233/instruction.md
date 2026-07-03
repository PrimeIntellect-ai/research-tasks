You are an IT support technician resolving a ticket for the Data Science team. 

**Ticket Description:**
"Our daily batch job (`stats_calculator.py`) is crashing with a Segmentation Fault. It is supposed to calculate the variance of 50 datasets. Right before it crashes, we noticed it outputs a mathematically impossible negative variance. We need to know exactly which file is causing this, what the anomalous value was, and where the code is crashing."

**Environment:**
- The script is located at `/home/user/app/stats_calculator.py`.
- The data files are in `/home/user/data/` (named `data_00.csv` to `data_49.csv`).
- The job was run and its standard output, standard error, and `faulthandler` trace were captured in `/home/user/logs/job.log`.
- An `strace` of the run was also captured in `/home/user/logs/strace.log`.

**Your Task:**
1. Inspect the logs and the code to investigate this statistical anomaly and crash.
2. Identify the specific data file that caused the crash.
3. Identify the exact anomalous (negative) variance value printed to the log.
4. Identify the line number in `/home/user/app/stats_calculator.py` that triggered the segmentation fault (the memory access violation).

Write your findings to a JSON file at `/home/user/resolution.json` with the following exact keys and types:
- `"faulty_file"`: (string) The name of the file (e.g., `"data_xx.csv"`).
- `"anomalous_variance"`: (float) The negative variance value printed.
- `"crash_line"`: (integer) The line number in `stats_calculator.py` where the fatal fault occurred.