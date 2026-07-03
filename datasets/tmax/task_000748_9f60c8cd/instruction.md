You are a data scientist tasked with cleaning up a server telemetry dataset using only standard Linux command-line tools (Bash built-ins, awk, sed, sort, etc.). Do not use Python, Perl, or any other scripting languages.

Our nightly ETL job failed and retried several times, resulting in a messy, pipe-separated (`|`) log file located at `/home/user/raw_telemetry.txt`. The file contains server CPU usage logs, but it has duplicates, is out of chronological order, and is in a "long" format. 

The columns in the raw file are: `timestamp|server_name|cpu_usage`

Your objective is to process this file into a clean, analytical CSV file located at `/home/user/smoothed_wide.csv`.

Perform the following operations in your pipeline:
1. **Deduplication & Sorting:** Remove any exact duplicate rows. Sort the remaining records chronologically by `timestamp` (which is an integer).
2. **Rolling Aggregation:** For each server individually, calculate a 3-step rolling average of the `cpu_usage`. 
   - If there is only 1 data point so far, the average is just that data point.
   - If there are 2 data points, it is the average of those two.
   - If there are 3 or more, it is the average of the *current* and *previous two* data points.
3. **Wide-Long Reshaping (Pivoting):** Convert the dataset from long format to wide format. The final output must be comma-separated (`csv`).
4. **Formatting:** The first row of your output file must be the header: `timestamp,alpha,beta,gamma`.
   - The subsequent rows must contain the timestamp and the rolling average for each server.
   - All rolling averages must be formatted to exactly one decimal place (e.g., `20.0`, `26.7`). Use standard half-up rounding if necessary.

**Example Input:**
```
1|alpha|10
1|beta|20
2|alpha|20
1|alpha|10
```
*(Notice the out-of-order and duplicated `1|alpha|10`)*

**Example Output:**
```
timestamp,alpha,beta,gamma
...
```

Write your commands directly in the terminal to produce the final `/home/user/smoothed_wide.csv` file.