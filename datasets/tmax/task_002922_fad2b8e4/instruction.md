You are an engineer managing a configuration tracking system. Recently, an upstream ETL job that ingests configuration changes experienced a failure and was automatically retried. As a result, the raw log file contains duplicate records and slightly time-skewed redundant entries for the same configuration keys.

Your task is to write a C program to process these logs and a bash script to orchestrate the pipeline. 

The raw log file is located at: `/home/user/raw_config_logs.txt`

The format of each line in the log file is:
`[EPOCH_TIMESTAMP] CONFIG_KEY=VALUE IP_ADDRESS`

Example:
`[1700000000] MAX_CONNS=100 192.168.1.15`

You must create a C program at `/home/user/process_logs.c` that reads this format from standard input (`stdin`) and writes to standard output (`stdout`). The C program must perform the following operations:

1. **Time-based Bucketing & Deduplication:** 
   Group the logs into 1-hour (3600 seconds) windows based on the epoch timestamp. The window start time is calculated as `(epoch / 3600) * 3600`.
   Because of the ETL retry issue, there may be multiple entries for the same `CONFIG_KEY` within the same 1-hour window. You must deduplicate these by keeping ONLY the record with the **largest (latest)** epoch timestamp for that key in that specific window.

2. **Data Masking:** 
   Anonymize the `IP_ADDRESS` by replacing the last octet (everything after the last `.`) with `XXX`. For example, `192.168.1.15` becomes `192.168.1.XXX`.

3. **Output Formatting:**
   The C program should output the deduplicated, masked records in CSV format:
   `WINDOW_START_EPOCH,CONFIG_KEY,VALUE,MASKED_IP`
   (The order of the output lines from the C program does not matter, as the bash script will sort them).

After writing the C program, create a bash script at `/home/user/run_pipeline.sh` that does the following:
1. Compiles `/home/user/process_logs.c` into an executable named `process_logs` in the same directory using `gcc`.
2. Pipes the contents of `/home/user/raw_config_logs.txt` into the compiled executable.
3. Sorts the resulting CSV output numerically by `WINDOW_START_EPOCH` (ascending), and then alphabetically by `CONFIG_KEY` (ascending).
4. Saves the final sorted output to `/home/user/processed_logs.csv`.

Ensure your bash script has executable permissions (`chmod +x`). Run your bash script to produce the final `/home/user/processed_logs.csv` file.