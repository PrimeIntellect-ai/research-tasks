You are a log analyst investigating patterns in a web server's access logs. The raw log file is corrupted, and you need to build an automated data processing pipeline to clean, anonymize, and aggregate the data.

You have been provided with a raw CSV log file at `/home/user/server_logs.csv`. 
The file does not have a header. Each line contains:
`timestamp,user_id,ip_address,response_time`

Some `response_time` values are missing (represented by an empty string, e.g., `16200,U01,10.0.0.1,`).

Your objective is to create a multi-stage data processing pipeline using Bash and a C program.

Step 1: Write a C program `/home/user/process_logs.c` that reads from standard input and writes to standard output. It must perform the following line-by-line transformations:
1. **Data Masking (Anonymization):** Mask the IPv4 addresses by replacing the last two octets with `*.*`. For example, `192.168.1.5` must become `192.168.*.*`.
2. **Imputation:** For missing `response_time` values, you must impute the value. Assuming the input data is already sorted by `user_id` and then by `timestamp`, replace a missing `response_time` with the *most recent valid response_time* for that specific `user_id`. If the very first record for a `user_id` is missing a response time, impute it as `0`.

Step 2: Write a bash orchestration script `/home/user/run_pipeline.sh` that performs the following steps:
1. Sorts the raw `/home/user/server_logs.csv` data. It must be grouped (sorted) by `user_id` (alphabetically) and then by `timestamp` (numerically ascending).
2. Compiles your C program (`gcc -O2 /home/user/process_logs.c -o /home/user/process_logs`).
3. Pipes the sorted data into your C program.
4. Saves the output of the C program to `/home/user/anonymized_logs.csv`. The output format must exactly match the input structure, but with masked IPs and imputed response times: `timestamp,user_id,masked_ip,response_time`.
5. Parses the `/home/user/anonymized_logs.csv` to calculate the average response time for each user.
6. Outputs the top 3 users with the highest average response times to `/home/user/top_users.txt`. The format must be `user_id,average_response_time` (average formatted to exactly 2 decimal places, e.g., `U01,166.67`). If there are ties in the average, sort them by `user_id` ascending.

Ensure `/home/user/run_pipeline.sh` is executable and run it to produce the final artifacts.