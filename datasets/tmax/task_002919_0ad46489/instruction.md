You are a data analyst working with server telemetry data. You have a raw time-series CSV file located at `/home/user/telemetry.csv` containing messy log messages. 

The CSV format is: `timestamp,hostname,raw_message`
Example row: `1696150800,srv-01,System status normal | CPU:45% | Mem:8GB`

Your task is to build a small automated data pipeline:

1. **C++ Feature Extractor**: Write a C++ program at `/home/user/extractor.cpp` that reads this CSV format from standard input. It must:
   - Tokenize the `raw_message` field.
   - Extract the CPU percentage (the integer value immediately following `CPU:` and preceding `%`).
   - Normalize the output by printing a new CSV format to standard output: `timestamp,hostname,cpu_percentage` (where `cpu_percentage` is just the integer).
   - Compile this program to `/home/user/extractor`.

2. **Pipeline Script**: Write a bash script at `/home/user/process.sh` that:
   - Uses your compiled `/home/user/extractor` to process `/home/user/telemetry.csv`.
   - Uses standard Unix tools (like `sort`) to sort the output by the extracted `cpu_percentage` in descending (highest first) numerical order.
   - Takes the top 5 records and saves them to `/home/user/top_cpu.csv`.

3. **Scheduling**: Create a cron configuration file at `/home/user/telemetry.cron` that schedules `/bin/bash /home/user/process.sh` to run precisely at the top of every hour (minute 0).

Ensure that your bash script is executable and that you manually run `/home/user/process.sh` once so that `/home/user/top_cpu.csv` is generated for verification.