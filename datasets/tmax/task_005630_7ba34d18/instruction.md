I have a corrupted CSV dataset of system logs located at `/home/user/raw_logs.csv`. The file has three columns: `timestamp`, `user_id`, and `log_message`. Some of the `log_message` fields are enclosed in double quotes and contain embedded newline characters (`\n`), which has been breaking our standard text processing tools. 

I need you to write a C program, saved as `/home/user/clean_logs.c`, that performs the following pipeline:

1. **Parse the CSV correctly**: Read the file, properly handling commas and embedded newlines inside double-quoted `log_message` fields.
2. **Data Cleaning**: Replace any embedded newline characters (`\n`) within the `log_message` fields with a single space (` `). Remove the surrounding double quotes from the output. Drop any rows where the `log_message` is entirely empty (after removing quotes).
3. **Feature Extraction (Similarity Computation)**: For each valid row, compute the Levenshtein distance between the cleaned `log_message` and the reference string `"SYSTEM_STARTUP_SEQUENCE_INITIATED"`.
4. **Sorting**: Sort all the valid records in ascending order based on the `timestamp` (which is a standard UNIX epoch integer).
5. **Changepoint/Anomaly Detection**: After sorting, compare the Levenshtein distance of each row to the *previous* row's distance. If the absolute difference is strictly greater than 10, flag the current row as an anomaly (`is_anomaly = 1`). Otherwise, `is_anomaly = 0`. The first row in the sorted output should always have `is_anomaly = 0`.
6. **Output**: Write the processed data to `/home/user/cleaned_logs.csv` with the following columns in exactly this order: `timestamp,user_id,cleaned_log_message,distance,is_anomaly`. Do not include a header row in the output file.

Compile your program to an executable named `/home/user/clean_logs` using `gcc -O3`, and run it. Ensure the output file is generated correctly.