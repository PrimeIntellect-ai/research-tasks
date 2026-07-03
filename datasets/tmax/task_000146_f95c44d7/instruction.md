You are tasked with building a robust data extraction and aggregation step for an ETL pipeline in C. 

A upstream system has dumped a dataset into `/home/user/data.csv`. The file contains 500,000 rows of telemetry data with a header row `id,value`. 
- `id` is a standard 32-bit integer.
- `value` is a 64-bit signed integer.

However, the upstream system occasionally fails to record a value. In these cases, the `value` field might be completely empty (e.g., `105,`) or contain the string `NaN` (e.g., `106,NaN`).

Your task is to write a C program that processes this dataset safely, avoiding any silent type coercion (like mistakenly parsing missing values as `0` or losing precision by casting large integers to floats).

Requirements:
1. Write a C program at `/home/user/process_data.c`.
2. The program must read `/home/user/data.csv`.
3. It must ignore any row where the `value` is missing, empty, or equals `NaN`.
4. It must compute three metrics from the *valid* rows:
   - The total count of valid rows.
   - The absolute maximum `value` (exact 64-bit precision).
   - The absolute minimum `value` (exact 64-bit precision).
5. Compile your program to an executable at `/home/user/etl_parser`.
6. Run your program and redirect its output to `/home/user/etl_result.txt`. 

The output format written to `/home/user/etl_result.txt` MUST exactly match this format:
Valid: <count>
Max: <max>
Min: <min>

Ensure your compilation is done with `gcc -O3 -Wall`.