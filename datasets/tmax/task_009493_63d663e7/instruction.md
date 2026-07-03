You are a data analyst tasked with processing a time-series CSV file containing server hardware metrics. 

The input file is located at: `/home/user/metrics.csv`

It has the following columns:
`timestamp,server_id,temperature,cpu_load,status_msg`

Your goal is to write a Python script that processes this file and outputs a cleaned, sampled, and aggregated version to `/home/user/processed_metrics.csv`.

Here are the strict processing requirements:

1. **Constraint-based Validation**: 
   - Discard any rows where `temperature` is strictly less than `0.0` or strictly greater than `120.0`.
   - Discard any rows where `cpu_load` is strictly less than `0.0` or strictly greater than `100.0`.
   - Discard rows with empty or missing values in any column.

2. **Tokenization and Normalization**:
   - Create a new column called `normalized_status` based on `status_msg`.
   - Convert the string to lowercase.
   - Remove all characters EXCEPT lowercase letters (a-z), numbers (0-9), and spaces.
   - Replace any sequence of multiple spaces with a single space, and strip leading/trailing whitespace.

3. **Data Sampling and Stratification**:
   - Extract the `date` (YYYY-MM-DD format) from the `timestamp` (which is in ISO 8601 format, e.g., `2023-10-24T14:30:00Z`).
   - For each unique `date` and `server_id` combination, keep ONLY the chronologically earliest valid reading.

4. **Sorting and Output**:
   - The output CSV must have exactly these columns: `date,server_id,temperature,cpu_load,normalized_status`
   - Sort the final output by `date` ascending, and then by `server_id` ascending.
   - Write the result to `/home/user/processed_metrics.csv` (include a header row).

Use standard Python libraries (e.g., `csv`, `re`, `datetime`). You can execute your script from the terminal to generate the final file.