You are acting as a configuration management assistant. We have a system that logs the hardware and software configuration limits of our database servers every few minutes. The data is exported to `/home/user/raw_configs.csv`.

The input CSV has the following wide-format schema (with a header row):
`Timestamp,ServerID,CPUCores,MemGigabytes,MaxConnections`
Example row:
`2023-11-01T08:15:30,srv-01,8,64,1500`

However, the logging agent sometimes glitches, producing corrupted rows (e.g., negative numbers, empty fields, or non-numeric values).

Your task is to build a Bash-only pipeline (using standard tools like `awk`, `sed`, `grep`, `sort`, etc. — do NOT use Python, Perl, or Ruby) to process this file and generate an aggregated report at `/home/user/hourly_config_stats.csv`.

Follow these specific data processing steps:
1. **Validation Checkpoint**: Filter out the header row and any invalid rows. A row is valid ONLY IF it has exactly 5 comma-separated columns, and the `CPUCores`, `MemGigabytes`, and `MaxConnections` fields are all strictly positive integers (greater than 0, digits only).
2. **Wide-to-Long Reshaping**: Convert the valid rows from wide format to long format. Each valid input row should produce three output records. The metric names should be exactly `CPU`, `MEM`, and `CONN`.
   Format: `Timestamp,ServerID,Metric,Value`
3. **Time-Based Bucketing**: Truncate the `Timestamp` to the hour. For example, `2023-11-01T08:15:30` becomes `2023-11-01T08`.
4. **Mathematical Aggregation**: Group the long-format data by `Hour`, `ServerID`, and `Metric`. Calculate the arithmetic mean (average) of the `Value` for each group.
5. **Formatting and Sorting**: The output file `/home/user/hourly_config_stats.csv` must NOT have a header. Each row must follow the format `Hour,ServerID,Metric,Average`. The `Average` must be formatted to exactly two decimal places (e.g., `8.00`, `1550.50`). Sort the final file alphabetically/lexicographically by `Hour` (ascending), then `ServerID` (ascending), then `Metric` (ascending).

Write a script or use the command line directly to produce the `/home/user/hourly_config_stats.csv` file.