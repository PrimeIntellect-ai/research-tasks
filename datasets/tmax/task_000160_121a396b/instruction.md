You are acting as a configuration manager tracking changes across thousands of server configuration snapshots. The snapshots are stored in a SQLite database, but analyzing the changes between consecutive snapshots using our legacy tool is too slow.

Your task is to orchestrate a data extraction pipeline, reverse-engineer a legacy black-box tool's logic, and write a high-performance C program to process the data.

**Requirements:**
1. **Database Export:** The database is located at `/data/configs.db`. It contains a table `snapshots` with two columns: `id` (INTEGER) and `content` (TEXT). Write a script or command to perform a bulk export of these configurations into a directory `/home/user/configs/`, naming each file `<id>.txt` (e.g., `1.txt`, `2.txt`, formatted with leading zeros if you prefer, but the C program must process them in numerical ID order).
2. **Reverse Engineer the Oracle:** You have been provided a stripped binary at `/app/config_diff_oracle`. It takes two config files as arguments (`/app/config_diff_oracle fileA.txt fileB.txt`) and outputs summary statistics of the changes (added, removed, modified) while masking and separately aggregating changes to sensitive keys. Use this oracle to understand the exact comparison logic, how sensitive keys are identified, and the specific output format.
3. **High-Performance Implementation:** Write a C program `/home/user/fast_tracker.c` and compile it to `/home/user/fast_tracker`. This program must take the directory of extracted configs as input, process them in numerical order (comparing snapshot 1 to 2, 2 to 3, etc.), and print the difference metrics for each consecutive pair in the *exact same format* as the oracle. At the very end, it must print a `TOTAL` line aggregating all metrics.
4. **Pipeline Orchestration & Logging:** Create a main bash script `/home/user/pipeline.sh` that orchestrates the entire workflow (database export -> compilation -> running the C program). The pipeline must implement logging to `/home/user/pipeline.log` noting the start and completion times of the "EXPORT" and "PROCESS" phases.
5. **Execution:** Run your pipeline. The output of your C program must be redirected to `/home/user/summary_stats.log`.

**Evaluation Constraints:**
- Your output in `/home/user/summary_stats.log` must exactly match the output of calling the oracle sequentially on the same pairs.
- Your C program's execution time will be measured against a reference baseline (calling the oracle in a bash loop). You must achieve a **speedup of at least 10x**.
- You must rely solely on C and standard bash tools.