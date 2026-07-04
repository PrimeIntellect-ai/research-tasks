You are a data engineer tasked with building the first stage of an ETL pipeline for a global messaging platform. You need to process a mixed-format log file containing multi-lingual text and structured data, validate it, and extract anomalies.

Your task is to write and execute a C++ program that processes `/home/user/raw_logs.txt`. 

### Input Data Format
Each line in `/home/user/raw_logs.txt` has the following format:
`[{TIMESTAMP}] {LOG_LEVEL} {JSON_PAYLOAD}`
Example:
`[2023-10-01T10:00:00Z] INFO {"user": "u1", "msg": "Hello 世界", "declared_len": 8}`

### Processing Requirements
Your C++ program must perform the following steps sequentially for each line:

1. **Information Extraction**: Parse the line to extract the Timestamp and the JSON payload. Ignore lines where the `LOG_LEVEL` is `ERROR`.
2. **Data Validation & Unicode Processing**: 
   - Parse the JSON payload. (You may download a header-only library like `nlohmann/json.hpp` into `/home/user/` to help with this).
   - Ensure the JSON contains the keys `"user"`, `"msg"`, and `"declared_len"`.
   - Calculate the actual number of **Unicode code points** in the `"msg"` string.
   - **Constraint**: If the actual number of Unicode code points does not exactly equal `"declared_len"`, the record is invalid. Drop invalid records.
3. **Anomaly Detection**:
   - For valid records, keep track of a Simple Moving Average (SMA) of the `"declared_len"` of the **last 5 valid messages** (including the current one). For the first 4 valid messages, calculate the average using the available valid messages.
   - **Changepoint/Anomaly**: If the current valid message's `"declared_len"` is strictly greater than `2.0 * (SMA excluding the current message)`, it is an anomaly. (Note: Anomalies still count towards the SMA for future messages. For the very first message, it cannot be an anomaly).

### Output Requirements
Your C++ program should produce two files:

1. `/home/user/clean_data.jsonl`: A JSON Lines file containing the valid payloads (just the JSON part), exactly as they appeared in the input.
2. `/home/user/anomalies.csv`: A CSV file logging the anomalies. The format must be exactly:
   `timestamp,user,declared_len`
   Include a header row.

Write the C++ code, compile it (e.g., using `g++ -std=c++17`), and run it to produce the required output files.