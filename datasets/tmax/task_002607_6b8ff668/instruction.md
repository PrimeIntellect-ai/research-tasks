You are tasked with processing a dataset of configuration changes collected from various servers. The data is provided in two different formats and needs to be cleaned, deduplicated, cryptographically signed with our proprietary tool, and aggregated into time buckets.

The data is located at:
1. `/home/user/data/configs.csv` (Columns: `timestamp` in "YYYY-MM-DD HH:MM:SS" UTC, `server_id`, `config_val`)
2. `/home/user/data/configs.json` (Array of objects with keys `time` as Unix epoch integer, `server`, `val`)

Your pipeline must perform the following steps:
1. **Data Ingestion & Normalization**: Read both files and normalize the fields. All timestamps should be converted to ISO8601 strings in UTC (e.g., "2023-10-01T12:00:00Z"). 
2. **Time-based Bucketing & Deduplication**: Group the records into 1-hour time buckets based on their timestamp (e.g., 12:00:00 to 12:59:59 belongs to the "12:00:00Z" bucket). If multiple records have the exact same `server_id` and `config_val` (or `server` and `val`) within the same 1-hour bucket, keep only the earliest one.
3. **Signature Generation**: Compute a signature for each unique, deduplicated `config_val`. We provide a proprietary compiled tool at `/app/config_hasher` which takes the `config_val` string as a single command-line argument and prints an 8-character hex signature. 
4. **Aggregation**: Save the final aggregated data to `/home/user/output/aggregated.json`. The output must be a JSON object mapping the start time of each 1-hour bucket (e.g., "2023-10-01T12:00:00Z") to a list of the computed hex signatures for that bucket. The list of signatures within each bucket must be sorted alphabetically.

**Performance Constraint**:
The dataset contains tens of thousands of records. Invoking the `/app/config_hasher` binary as a subprocess for every single record will result in significant overhead and will fail the performance evaluation. 
To pass the evaluation, you must analyze the stripped binary `/app/config_hasher`, reverse-engineer its simple hashing algorithm, and reimplement it natively in your Python script to achieve high throughput. 

Write your complete processing pipeline in `/home/user/process.py`. When run, it should read the inputs, process them, and generate `/home/user/output/aggregated.json`.