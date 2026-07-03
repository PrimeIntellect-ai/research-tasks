You are an AI assistant helping a data scientist clean and aggregate a dirty telemetry log file. 

You have been provided with a raw log file located at `/home/user/telemetry.txt`. Each line in the file represents a sensor reading and follows this format:
`[TIMESTAMP] [VALUE] [STATUS_MESSAGE]`

Example lines:
`2023-10-12T08:14:05Z 45.2 OK`
`2023-10-12T08:29:55Z 46.1 FAIL: timeout`

Your task is to write a C++ program (`/home/user/process.cpp`) that reads this file and performs time-based bucketing and aggregation. Specifically, you must:

1. **Timestamp Alignment**: Parse the ISO 8601 timestamp and truncate/align it to the start of the hour (e.g., `2023-10-12T08:14:05Z` becomes the bucket `2023-10-12T08:00:00Z`).
2. **Aggregation**: For each hourly bucket, calculate:
   - The mean (average) of the numeric `[VALUE]`s.
   - The total count of records in that hour where the `[STATUS_MESSAGE]` contains the exact substring `FAIL`.
3. **Output Generation**: Write the aggregated results to a CSV file at `/home/user/aggregated.csv`. 
   - The CSV must have the header row: `Hour,MeanValue,FailCount`
   - The rows must be sorted chronologically.
   - The `MeanValue` must be formatted to exactly 1 decimal place.
4. **Pipeline Logging**: Append a single log line to `/home/user/pipeline.log` in the exact format: `Processed <N> records. Found <M> unique hours.`, where `<N>` is the total number of lines read, and `<M>` is the number of distinct hourly buckets.

Requirements:
- Write the C++ code in `/home/user/process.cpp`.
- Compile it using `g++ -O2 /home/user/process.cpp -o /home/user/process`.
- Run the compiled binary to generate the required outputs.

Ensure your program handles the exact file paths mentioned and correctly handles string parsing. Standard C++17 or C++20 features are sufficient.