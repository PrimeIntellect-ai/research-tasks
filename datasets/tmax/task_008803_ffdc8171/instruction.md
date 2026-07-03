You are a log analyst investigating patterns in a fleet of IoT thermal sensors. The raw logs have been corrupted: some readings are missing, some entries have invalid HTTP-like status codes, and some lines contain malformed sensor IDs.

You need to build a multi-stage data processing pipeline using Bash and C to clean, impute, and filter these logs.

**Input Data:**
A raw log file is located at `/home/user/raw_sensor_logs.txt`.
Each line is comma-separated: `timestamp,sensor_id,temperature,status`
* `timestamp`: Unix epoch integer.
* `sensor_id`: String identifier.
* `temperature`: Float reading. Sometimes corrupted and represented as `-`.
* `status`: Integer status code.

**Task Requirements:**

1. **Bash Pipeline Orchestration & Regex Filtering:**
   Write a bash script at `/home/user/process_logs.sh`. This script must compile your C program (described below) and execute a pipeline that does the following:
   * Reads `/home/user/raw_sensor_logs.txt`.
   * Uses `grep` to filter out any lines where the `sensor_id` does NOT exactly match the regex pattern: `SENS-[A-Z]{3}-[0-9]{4}` (e.g., `SENS-ABC-1234` is valid, `SENS-aBC-123` is not).
   * Pipes the filtered output into your compiled C program.
   * Redirects the standard output of the C program to `/home/user/clean_logs.csv`.

2. **C Program (Validation & Imputation):**
   Write a C program at `/home/user/imputer.c` that reads from standard input (STDIN) and performs the following:
   * **Constraint-based Validation:** Parse the `status` field. If the `status` is NOT between `100` and `599` (inclusive), completely discard the line.
   * **Interpolation/Imputation:** If the `temperature` is missing (represented as exactly `-`), impute it using the *last valid temperature that was successfully emitted to STDOUT*. If the very first valid line has a missing temperature, default the imputed value to `20.0`. Imputed temperatures should be formatted to 1 decimal place.
   * **Output:** Print the cleaned and imputed lines to standard output (STDOUT) in the exact same `timestamp,sensor_id,temperature,status` CSV format. Floating point numbers should be formatted to 1 decimal place (e.g., `22.5`).
   * **Pipeline Logging:** When the program finishes reading STDIN (EOF), it must append a single line to `/home/user/pipeline.log` with exactly this format:
     `Discarded: X, Imputed: Y`
     (Where X is the number of lines discarded due to invalid status codes, and Y is the number of missing temperatures successfully imputed. Do not count lines filtered out by `grep` in X).

Ensure your script `/home/user/process_logs.sh` is executable and can be run without arguments to process the data from start to finish.