You are an automation specialist tasked with building a high-performance C-based ETL pipeline to process messy system logs. 

System logs are currently being exported to `/home/user/raw_logs.csv` with the following header:
`timestamp,ip_address,message`
The timestamp format is `YYYY-MM-DD HH:MM:SS`. 
The `message` field is enclosed in double quotes. 

Due to a bug in the upstream logging system, some log messages contain embedded newline characters (`\n`) within the quotes. Your pipeline must strictly identify and **silently drop any row that contains an embedded newline** anywhere in the record.

You need to build a pipeline that does the following:
1. **Clean and Extract**: Read the CSV. Drop any row containing an embedded newline. For the surviving rows, extract the hour bucket from the timestamp (e.g., `2023-10-15 14`), calculate the string length of the `message` (excluding the surrounding quotes), and determine if the message contains the exact uppercase substring `"ERROR"`.
2. **Aggregate**: Group the cleaned data by the hour bucket. Calculate the total number of events, the total number of `"ERROR"` events, and the average message length (formatted to exactly two decimal places, e.g., `45.50`) for each hour.
3. **Orchestrate**: Create a pipeline to compile and run this process.

**Deliverables:**
Create a directory `/home/user/etl_pipeline/` containing:
1. `clean_extract.c`: A C program that reads the raw CSV from standard input (`stdin`) and outputs intermediate extracted features to `stdout`.
2. `aggregate.c`: A C program that reads the sorted intermediate data from `stdin` and outputs the final aggregated statistics to `stdout`.
3. `Makefile`: A makefile to compile `clean_extract` and `aggregate` using `gcc -O2`.
4. `run.sh`: A bash script that uses the compiled C binaries and standard Linux utilities (like `sort`) to process `/home/user/raw_logs.csv` and write the final output to `/home/user/aggregated_stats.csv`.

**Output Format Constraint:**
The final `/home/user/aggregated_stats.csv` must include a header and be formatted exactly as:
`hour,total_events,error_count,avg_msg_len`
Example row:
`2023-10-15 14,150,12,42.00`

Ensure your C code is robust enough to handle the CSV parsing manually, as standard libraries for CSV don't exist in base C. The embedded newlines will always be inside the double quotes of the `message` column. Make sure `run.sh` is executable.