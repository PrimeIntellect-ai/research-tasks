You are tasked with building a configuration tracking pipeline. As a configuration manager, you receive irregular snapshot events of a system's configuration parameters over time. You need to normalize this data, compute the system's "drift" from a known baseline, and orchestrate the data flow.

You have a raw log file located at `/home/user/raw_configs.txt`. Each line contains a time-series event for three numeric configuration parameters in the format: `timestamp,paramA,paramB,paramC`. The timestamps are in seconds but arrive at irregular intervals.

Your baseline (ideal) configuration state is:
- paramA = 50
- paramB = 100
- paramC = 150

**Task Requirements:**

1. **Write a C program** at `/home/user/process_drift.c` that reads the CSV format from standard input.
2. The C program must **resample and gap-fill** the data to create regular snapshots every 10 seconds, starting exactly at `t=0` and ending at `t=100` inclusive (i.e., `0, 10, 20, 30, ... 100`).
3. For each 10-second interval:
    - If a target timestamp does not exist in the input, perform **linear interpolation** based on the closest available timestamps before and after the target time.
    - If the target timestamp is *before* the first available timestamp, use the values of the first available timestamp (flat extrapolation).
    - If the target timestamp is *after* the last available timestamp, use the values of the last available timestamp (flat extrapolation).
    - Round the interpolated parameter values to the nearest integer (standard half-up rounding).
4. For each resampled interval, compute the **Euclidean distance** (drift) between the interpolated parameters `(A, B, C)` and the baseline `(50, 100, 150)`.
5. The C program should output to standard output in the following CSV format:
   `timestamp,interpolated_A,interpolated_B,interpolated_C,drift_score`
   *Note: Format the `drift_score` to exactly 2 decimal places.*
6. **Create a bash script** at `/home/user/pipeline.sh` that:
    - Compiles the C program into an executable named `process_drift` (ensure you link the math library).
    - Pipes the contents of `/home/user/raw_configs.txt` into the compiled program.
    - Redirects the standard output of the program to `/home/user/drift_report.csv`.

Ensure your scripts are executable and run without errors. The system will inspect `/home/user/drift_report.csv` to verify your implementation.