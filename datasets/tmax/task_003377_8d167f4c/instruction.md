You are tasked with fixing a messy configuration tracking pipeline. An ETL job that scrapes server configuration updates crashed and was retried, resulting in a dump file that contains duplicate records. Furthermore, the log file originates from a legacy Windows subsystem, so it is not in standard UTF-8, and some timestamp entries were lost and marked as `[MISSING]`.

You have two input files:
1. `/home/user/data/server_configs.log`
   - Encoded in **UTF-16LE**.
   - Contains unstructured text lines logging package updates. 
   - Example line: `[2023-11-02 08:30:00] CONFIG_UPDATE: ServerID:Srv-Alpha upgraded package 'nginx' to version:v1.18.0`
   - Sometimes the timestamp is missing: `[MISSING] CONFIG_UPDATE: ServerID:Srv-Beta upgraded package 'redis' to version:v6.2.5`
   - Due to the ETL retry bug, there are exact duplicate events (though spacing might vary slightly in the raw text).

2. `/home/user/data/server_meta.csv`
   - Standard UTF-8 CSV file containing metadata for the servers.
   - Columns: `ServerID,IP_Address,Datacenter`

Your goal is to write a Python script that processes this data and produces a clean, deduplicated JSON file at `/home/user/output/clean_configs.json`.

The script must perform the following:
1. **Read and Extract**: Read the log file with the correct encoding. Use Regular Expressions to extract the `Timestamp` (or `MISSING`), `ServerID`, `Package`, and `Version` from each line. Ignore lines that do not match the `CONFIG_UPDATE` pattern.
2. **Impute**: For any record where the timestamp is `[MISSING]`, impute (forward-fill) the timestamp using the most recently parsed valid timestamp from the file reading top-to-bottom.
3. **Deduplicate**: Remove duplicate configuration updates. A record is considered a duplicate if it has the exact same imputed timestamp, ServerID, Package, and Version as another record.
4. **Join**: Merge the deduplicated records with `server_meta.csv` based on `ServerID` to get the `IP_Address`. Discard any records for which the `ServerID` is not found in the CSV.
5. **Output**: Save the result as a JSON array of objects to `/home/user/output/clean_configs.json`. 
   - Each object must have the following keys exactly: `"timestamp"`, `"server_id"`, `"ip_address"`, `"package"`, `"version"`.
   - Sort the final list of objects chronologically by `timestamp`. If timestamps are identical, sort alphabetically by `server_id`, then by `package`.
   - The JSON should be pretty-printed with a 2-space indent.

Create the `/home/user/output` directory if it does not exist. Your output will be verified automatically by comparing the final JSON file against the expected output.