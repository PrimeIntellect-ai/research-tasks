You are a log analyst investigating patterns in an ETL pipeline that frequently produces duplicate records upon retrying failed jobs. Your goal is to build a C++ based data processing pipeline that merges time-series log files, removes duplicates, masks sensitive data, standardizes timestamps, and implements a quality gate.

Here are the requirements:

1. **Input Files:**
   There are several CSV log files located in `/home/user/logs/`.
   Each file has the following header: `timestamp_ms,user_id,action,value`
   The `timestamp_ms` is a Unix epoch timestamp in milliseconds.

2. **C++ Processor (`/home/user/processor.cpp`):**
   Write a C++ program that reads multiple CSV files (passed as command-line arguments), processes them, and writes the output to a file specified by a `-o` flag.
   
   **Processing Logic:**
   - **Union/Merge:** Combine all records from all input files. The combined records must be processed in chronological order.
   - **Deduplication:** An ETL bug causes duplicates. A record is considered a duplicate if there is an *earlier* valid record with the **same `user_id` and `action`** within a **5-second (5000 ms) window** (inclusive). You must drop the duplicates and keep the earliest record in the window.
   - **Data Masking:** Anonymize the `user_id` by replacing it with `MASKED_` followed by the last 3 characters of the original `user_id` (e.g., `U12345` becomes `MASKED_345`). You can assume `user_id`s are always at least 3 characters long.
   - **Normalization:** Convert `timestamp_ms` to seconds (`timestamp_sec`).
   
   **Quality Gate:**
   - The program must calculate the drop rate: `(number of dropped duplicates) / (total number of input records)`.
   - If the drop rate is **strictly greater than 20%**, the program must print an error message to standard error and exit with status code `2` without writing the output file.
   - Otherwise, write the processed records to the output CSV and exit with status code `0`.

   **Output Format:**
   The output CSV must have the header: `timestamp_sec,masked_user_id,action,value`
   Records must be sorted by `timestamp_sec` in ascending order. If timestamps are identical, preserve the original order or sort by user_id (the provided test data won't have identical timestamps for valid records).

3. **Compilation:**
   Compile your program to `/home/user/processor` using `g++` (C++17 is available).

4. **Pipeline Script (`/home/user/run_pipeline.sh`):**
   Write a bash script that:
   - Executes `/home/user/processor` passing all `.csv` files in `/home/user/logs/` as inputs, and sets the output to `/home/user/processed_logs.csv`.
   - Checks the exit code of the C++ processor.
   - If the exit code is `0`, append the string `SUCCESS` to `/home/user/pipeline.log`.
   - If the exit code is `2`, append the string `QUALITY GATE FAILED` to `/home/user/pipeline.log`.

5. **Scheduling:**
   Create a cron schedule file at `/home/user/crontab.txt` that contains exactly one cron job line to execute `/home/user/run_pipeline.sh` every 15 minutes.

Note: Run the bash script `/home/user/run_pipeline.sh` manually once to ensure `/home/user/processed_logs.csv` and `/home/user/pipeline.log` are generated for verification.