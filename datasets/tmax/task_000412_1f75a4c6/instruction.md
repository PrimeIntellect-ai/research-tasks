You are an automation specialist managing an ETL pipeline. Recently, an upstream data job failed midway and was automatically retried, resulting in multiple raw data chunks containing overlapping (duplicate) records. To make matters worse, one of the legacy upstream systems outputs text in ISO-8859-1 encoding instead of UTF-8.

Your task is to write a highly performant C++ program that acts as a robust merge, deduplication, and normalization step in the ETL workflow. 

**Task Requirements:**
1. **Input Data:** Read three CSV files located at:
   - `/home/user/data/chunk_A.csv`
   - `/home/user/data/chunk_B.csv`
   - `/home/user/data/chunk_C.csv`
   The CSV files have the following columns: `event_id,timestamp,user_name,action`.

2. **Deduplication:** There are duplicate records across these files. You must deduplicate the records based on the `event_id` column. If multiple records share the same `event_id`, keep exactly one of them (they are identical in other fields aside from potential encoding differences; keeping any one is fine).

3. **Character Encoding Handling:** The `user_name` field in the input files contains a mix of standard ASCII and ISO-8859-1 encoded characters. Your program must convert all ISO-8859-1 characters in the `user_name` field to properly encoded UTF-8. *(Hint: Any byte value > 127 in the CSV can be assumed to be an ISO-8859-1 character. In ISO-8859-1, each character is 1 byte, which maps exactly to the first 256 Unicode code points).*

4. **Sorting:** The final aggregated dataset must be sorted primarily by `timestamp` (ascending) and secondarily by `event_id` (ascending, lexically).

5. **Parallel Processing:** You must utilize standard C++ parallel algorithms (`std::execution::par`) or standard threading (`std::thread`, `std::async`) to process the files, parse the lines, or sort the massive consolidated dataset to ensure high performance.

6. **Output:** Write the finalized, deduplicated, sorted, and UTF-8 normalized data to a new CSV file at `/home/user/output/clean_events.csv`. Ensure the output file includes the CSV header: `event_id,timestamp,user_name,action`.

**Execution:**
- Save your C++ source code as `/home/user/dedup_etl.cpp`.
- Compile it using exactly: `g++ -std=c++17 -O3 -pthread /home/user/dedup_etl.cpp -o /home/user/dedup_etl` (you may install standard development tools if necessary).
- Run your executable to generate `/home/user/output/clean_events.csv`.