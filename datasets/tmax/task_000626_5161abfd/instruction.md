You are a data engineer tasked with building a time-series ETL pipeline in C++.

We have two sensors dropping data into the `/home/user/data/` directory. 
1. The temperature sensor produces `/home/user/data/temp.csv`. For legacy reasons, this file is encoded in UTF-16LE. The columns are `timestamp,temperature` where `timestamp` is an integer Unix epoch (seconds).
2. The humidity sensor produces `/home/user/data/humidity.csv`. This file is encoded in standard UTF-8. The columns are `timestamp,humidity` where `timestamp` is a string in ISO 8601 format (e.g., `2023-10-12T08:00:00Z`).

Your task:
1. Write a C++ program at `/home/user/etl.cpp` that:
   - Reads both CSV files, correctly handling their respective character encodings.
   - Converts the ISO 8601 timestamps from the humidity data into integer Unix epochs (seconds).
   - Performs an INNER JOIN on the two datasets based on the exact Unix epoch timestamp.
   - Outputs the merged data to `/home/user/output/merged.csv` in UTF-8 encoding.
   - The output CSV must have the header `timestamp,temperature,humidity` and the rows must be sorted chronologically by timestamp.

2. Create a bash wrapper script at `/home/user/run_etl.sh` that compiles `/home/user/etl.cpp` (if not already compiled) into `/home/user/etl_bin` and executes it. Make sure the script is executable.

3. Schedule this pipeline to run automatically by adding an entry to the user's crontab. The cron job should execute `/home/user/run_etl.sh` every 15 minutes. 

Note: Ensure `/home/user/output/` exists before your program tries to write to it. Standard C++17 or C++20 libraries are available.