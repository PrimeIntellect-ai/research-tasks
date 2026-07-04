You are an ETL Data Engineer. We have a pipeline that processes two CSV sensor feeds: Temperature and Humidity. 

Currently, our pipeline is failing because the raw CSV files contain embedded newlines in the "Notes" column (which are properly enclosed in double quotes, per RFC 4180). Standard Unix tools and simple `std::getline` C++ implementations silently truncate or drop these rows, ruining the data integrity.

Your task is to write a robust C++ program that correctly parses these CSV files, performs time-based bucketing, aggregates the values, and joins the two data streams.

**Data Sources:**
1. `/home/user/data/temp.csv` - Columns: `timestamp`, `temperature`, `notes`
2. `/home/user/data/humidity.csv` - Columns: `timestamp`, `humidity`, `notes`

Timestamps are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-01T10:01:15Z`).

**Requirements:**
1. **Create a C++ program** at `/home/user/etl_pipeline.cpp`.
2. **Robust CSV Parsing:** Your program must correctly parse the CSV files, fully supporting embedded newlines within double-quoted fields. You may use standard C++ libraries only (no external libraries like Boost or csv-parser).
3. **Time-Based Bucketing:** Align the timestamps to the start of their **5-minute intervals**. For example:
   - `2023-10-01T10:01:15Z` -> `2023-10-01T10:00:00Z`
   - `2023-10-01T10:06:05Z` -> `2023-10-01T10:05:00Z`
4. **Aggregation:** Calculate the average `temperature` and average `humidity` for each 5-minute bucket. 
5. **Join:** Perform an INNER JOIN on the 5-minute bucket timestamps. Only buckets that have data from *both* sensors should be included in the output.
6. **Output:** Write the results to `/home/user/output/aligned_5min.csv` with the following exact header and format:
   `bucket,temp_avg,humidity_avg`
   
   Format the averages to exactly 2 decimal places. 

**Execution:**
Compile your code using `g++ -O2 -std=c++17 /home/user/etl_pipeline.cpp -o /home/user/etl_pipeline` and execute it. 
Ensure the final output file `/home/user/output/aligned_5min.csv` is correctly generated.