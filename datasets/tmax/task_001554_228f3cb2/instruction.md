You are a log analyst investigating user activity patterns. You have received a large, continuously appended log file containing system events in JSON-Lines format. However, the system that generated these logs has a known bug: it inconsistently encodes basic ASCII characters in the `username` field as Unicode escape sequences (e.g., encoding 'a' as `\u0061`), which breaks your standard parsing tools. 

Your task is to write a C++ program that streams this large log file, processes it, and generates both an anonymized log feed and an aggregated metrics report.

**Input:**
*   File: `/home/user/events.jsonl`
*   Format: Each line is a JSON object. Example: `{"timestamp": "2024-03-10T14:23:05Z", "username": "j\u0064oe", "action": "LOGIN"}`

**Processing Requirements:**
1.  **Streaming:** The program must read the file line-by-line to handle arbitrarily large files without loading the entire file into memory.
2.  **Unicode Decoding:** You must properly decode the `\uXXXX` sequences in the `username` field back to their standard ASCII characters. You can assume only basic ASCII characters (hex 0000 to 007F) will be escaped this way.
3.  **Data Masking:** Output a new file at `/home/user/anonymized.jsonl`. In this file, keep the JSON structure exactly the same, but replace the decoded value of `username` with exactly `***`. 
4.  **Timestamp Alignment & Time-Based Bucketing:** Parse the ISO 8601 timestamps (`YYYY-MM-DDTHH:MM:SSZ`) and align them to 1-hour buckets. The bucket label should be the Unix epoch time (in seconds) of the start of that hour.
5.  **Aggregation:** Keep a count of each `action` per 1-hour bucket.

**Outputs:**
1.  `/home/user/anonymized.jsonl`: The streamed, masked JSON-Lines file. (e.g., `{"timestamp": "2024-03-10T14:23:05Z", "username": "***", "action": "LOGIN"}`)
2.  `/home/user/aggregation.csv`: A CSV file containing the aggregated counts.
    *   Columns must be exactly: `bucket_epoch,action,count`
    *   The rows must be sorted in ascending order first by `bucket_epoch`, then alphabetically by `action`.

**Execution:**
*   You must write your solution in a file named `/home/user/process_logs.cpp`.
*   Compile it using standard C++17: `g++ -std=c++17 -O3 /home/user/process_logs.cpp -o /home/user/process_logs`
*   Execute the binary so that the output files are generated.