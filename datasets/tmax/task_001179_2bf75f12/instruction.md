You are a data engineer tasked with fixing and rebuilding an ETL pipeline. The current pipeline silently drops records from our monitoring system because it cannot handle embedded newlines in CSV files. 

Your task is to write a C++ program that correctly parses this messy CSV, reshapes the data, deduplicates it, performs simple changepoint detection, and outputs the results as JSON Lines (JSONL).

**Input Data:**
A raw CSV file is located at `/home/user/raw_metrics.csv`.
The CSV has the following header: `ts,hostname,cpu,mem,disk,event_log`
*   `ts`: integer Unix timestamp
*   `hostname`: string
*   `cpu`, `mem`, `disk`: float values (wide format)
*   `event_log`: A string that may contain embedded newline characters (`\n`). If it contains a newline, the entire field is enclosed in double quotes (`"`). There are no escaped quotes (`""`) inside the field.

**C++ Program Requirements:**
Create your C++ source file at `/home/user/process_metrics.cpp`. You must compile it to `/home/user/process_metrics` and run it. You may install and use `nlohmann-json3-dev` via `apt` for JSON serialization.

1.  **Parsing:** Read `/home/user/raw_metrics.csv`. You must correctly parse rows where the `event_log` field spans multiple lines due to embedded newlines inside double quotes.
2.  **Wide-to-Long Reshaping:** Convert the wide metrics (`cpu`, `mem`, `disk`) into a long format. For every parsed row, generate three separate records, one for each metric. The new fields should be `ts`, `hostname`, `metric_name` (e.g., "cpu"), `metric_value`, and `event_log`.
3.  **Hash-Based Deduplication:** Due to network retries, there are duplicate records. Construct a string key formatted as `<ts>_<hostname>_<metric_name>`. Calculate the `std::hash<std::string>` of this key. If you encounter a hash you've already seen, drop the record. Keep only the *first* occurrence.
4.  **Anomaly (Changepoint) Detection:** As you process the deduplicated records (in the order they appeared in the CSV), keep track of the *previous* `metric_value` for each unique `hostname` + `metric_name` combination. If the current `metric_value` is strictly greater than `3.0` times the previous value, flag this record as an anomaly. (The first observed value for a host+metric is never an anomaly).
5.  **Output Generation:** 
    *   Write ALL deduplicated long-format records to `/home/user/processed.jsonl`.
    *   Write ONLY the anomalous records to `/home/user/anomalies.jsonl`.
    *   Each line must be a valid JSON object with keys: `"ts"` (int), `"hostname"` (string), `"metric_name"` (string), `"metric_value"` (float), and `"event_log"` (string).

**Execution:**
Compile your program with `g++ -O3 -std=c++17 /home/user/process_metrics.cpp -o /home/user/process_metrics` and run it so the output files are generated.