You are tasked with building a configuration management ETL pipeline to track server configuration drift. Configuration changes are dumped by different legacy systems into a raw directory, using different formats and schemas. 

You must write a Python script at `/home/user/process_configs.py` that reads all files in `/home/user/raw_configs/`, cleans, normalizes, deduplicates the records, and writes the output to a canonical format.

Here are the requirements:

1. **Input Directory**: `/home/user/raw_configs/`. It contains a mix of JSON and CSV files.
2. **Normalization Rules**:
    * Each output record must be a JSON object with exactly four keys: `server`, `timestamp`, `key`, and `value`.
    * **Schema Mapping**:
        * Server name: Map `host_name` (JSON) and `server` (CSV) to `server`.
        * Timestamp: Map `event_time` (JSON) and `date` (CSV) to `timestamp`.
        * Config Key: Map `cfg_key` (JSON) and `key` (CSV) to `key`.
        * Config Value: Map `cfg_val` (JSON) and `value` (CSV) to `value`.
    * **Data Standardization**:
        * All `value` fields must be converted to strings (e.g., integer `100` becomes `"100"`).
        * All `timestamp` fields must be converted to ISO 8601 format with a `Z` suffix indicating UTC (e.g., `YYYY-MM-DDTHH:MM:SSZ`). The input date strings will either be in `YYYY-MM-DDTHH:MM:SSZ` or `YYYY/MM/DD HH:MM:SS` format (assume the latter is also UTC).
3. **Deduplication**: 
    * If multiple records across all files have the exact same `server`, `timestamp`, `key`, and `value` (after normalization), keep only one instance.
4. **Output**:
    * Write the deduplicated, normalized records as a JSON array to `/home/user/normalized_configs.json`.
    * The JSON array must be sorted chronologically by `timestamp`. If timestamps are identical, sort alphabetically by `server`, then by `key`.
5. **Pipeline Logging**:
    * The script must append a log line to `/home/user/pipeline.log` in the exact format: `[INFO] Processed <N> raw records. Exported <M> unique records.` where `<N>` is the total number of rows/objects read, and `<M>` is the count of deduplicated records written.

Run your script to process the data and generate the output files.