You are assisting a log analyst in investigating data anomalies from an ETL pipeline. The pipeline occasionally retries failed jobs, producing duplicate or corrupted records. We need a fast, parallelized data filter written in C to sanitize these logs and reshape them for downstream analysis.

An image containing the strict validation rules for the logs is located at `/app/etl_rules.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to extract the validation thresholds.

Your task is to write a C program at `/home/user/log_filter.c` and compile it to `/home/user/log_filter`. 

The program must take exactly one argument: the path to an input CSV file. 
The input CSV has the following wide format (with a header row):
`EventID,Timestamp,CPU_Usage,Memory_Usage,RetryCount`

Your C program must implement the following:
1. **Validation Checkpoints**: Check every row against the rules extracted from `/app/etl_rules.png`.
2. **Duplicate Detection**: Check for any duplicate `EventID` values within the single input file.
3. **Parallel Data Processing**: Use OpenMP (`#pragma omp`) to parallelize the validation of records.
4. **Wide-long format reshaping**: If the file passes all validation checks, reshape the data from wide to long format and print it to standard output. The output should have the format `EventID,Timestamp,MetricName,MetricValue` (where MetricName is either `CPU_Usage` or `Memory_Usage`). Do not print a header.
5. **Exit Codes**: 
   - If the file is completely valid (no rules violated, no duplicate EventIDs), output the long-format data to `stdout` and exit with code `0`.
   - If *any* row violates the rules or if there are duplicate `EventID`s, output nothing to `stdout` and exit with code `1` (or any non-zero exit code).

Compile your program ensuring OpenMP is enabled (`-fopenmp`). The system will evaluate your compiled `/home/user/log_filter` binary against a hidden dataset of valid and corrupted log files.