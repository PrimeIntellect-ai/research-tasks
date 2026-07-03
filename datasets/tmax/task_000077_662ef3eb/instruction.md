You are an automation specialist managing an ETL pipeline. A daily data extraction job occasionally fails and retries, creating files with duplicated records. Furthermore, a recent upstream security incident resulted in malformed/malicious records occasionally appearing in the data dumps.

Your task is to create a C++ data filter and deduplication tool that processes these CSV files.

First, examine the image located at `/app/etl_rules.png`. It contains the exact business logic and security rules for validating a record. You will need to extract the text from this image to understand what constitutes a "valid" vs "invalid" record.

Write a C++ program and save its source at `/home/user/filter.cpp`, then compile it to `/home/user/filter`. 

The program must be executable with the following signature:
`./filter <input_csv_path> <output_csv_path> <log_file_path>`

The input CSV files have the following header:
`TransactionID,CustomerName,Department,Amount`

Your program must perform the following:
1. **Validation**: Stream through the input CSV. If *any* record in the file violates the rules extracted from `/app/etl_rules.png`, the program must immediately abort, write nothing to the output, and exit with status code `1` (Reject).
2. **Deduplication & Normalization**: If the file contains no violating records, the program must deduplicate the records. A record is a duplicate if it has the exact same `TransactionID`. Keep the first occurrence and drop subsequent ones. 
3. **Pipeline Logging**: For every duplicate dropped, append a line to the `log_file_path` with the format: `Duplicate Dropped: <TransactionID>`.
4. **Success**: Write the deduplicated records (including the header) to `output_csv_path` and exit with status code `0` (Accept).

There is a test corpus of CSV files on the system to help you verify your solution:
- `/app/corpus/clean/`: Contains perfectly valid data files (though they may contain duplicates, which your program should handle and exit `0`).
- `/app/corpus/evil/`: Contains files where at least one row violates the security/business rules. Your program must reject these and exit `1`.

Ensure your C++ code is robust, correctly handles standard CSV reading, and precisely implements the rules from the image.