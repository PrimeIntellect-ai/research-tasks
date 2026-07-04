You are a data analyst tasked with processing a messy CSV file containing server log extracts. You need to extract structured metrics from unstructured text, normalize them, aggregate the results, and prepare a clean CSV file ready for database bulk import.

An input file is located at `/home/user/raw_logs.csv` with the following columns:
`server_id,report_text`

The `report_text` column contains free-text written by sysadmins. Hidden within this text are two key metrics:
1. CPU usage percentage (e.g., "45%")
2. Memory usage in Gigabytes (e.g., "12GB")

Your task is to write and execute a Python script that accomplishes the following pipeline:
1. **Extraction**: Parse the CPU percentage (integer before the `%` sign) and the Memory amount (integer before `GB`) from the `report_text` column for each row. 
2. **Normalization**: 
   - Convert the CPU percentage to a normalized float between 0.0 and 1.0 (e.g., 45% becomes 0.45).
   - Standardize the Memory into Megabytes (MB), assuming exactly 1024 MB per 1 GB.
3. **Aggregation**: Group the records by `server_id`. For each server, calculate:
   - The **average** of the normalized CPU usage (rounded to exactly 2 decimal places).
   - The **total sum** of the Memory in MB.
4. **Export**: Save the aggregated results to a new CSV file at `/home/user/db_import.csv`. The file must have exactly the following header:
   `server_id,avg_cpu_norm,total_mem_mb`
   Sort the output rows alphabetically by `server_id`.

Example of raw text: "The server experienced a spike to 90% CPU and is using 8GB of RAM." -> CPU: 90, Mem: 8.

Ensure your final output file is perfectly formatted as standard CSV, using commas as delimiters, so it can be bulk-loaded into a database.