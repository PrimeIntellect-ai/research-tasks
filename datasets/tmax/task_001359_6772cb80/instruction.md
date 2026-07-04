You are a data engineer tasked with fixing a broken ETL pipeline. The pipeline extracts multi-language sensor logs from a flaky upstream API, processes them, and loads them into a downstream data warehouse service.

Currently, the system is failing data quality checks. We have a set of services running on the machine, orchestrated by a local startup script:
1. **Sensor API (Producer)**: Runs on `http://localhost:5001`. The endpoint `/api/v1/logs` returns JSON lines of sensor data. This API is highly flaky and often drops connections mid-transfer.
2. **Redis**: Runs on `localhost:6379`. Available for caching, state tracking, or deduplication.
3. **Data Warehouse (Consumer)**: Runs on `http://localhost:5002`. Accepts cleaned JSON lines via POST to `/api/v1/load`.

Your predecessor wrote an initial Bash script located at `/home/user/etl_pipeline.sh`. It has three major flaws you must fix:
1. **Duplicate Records on Retry**: Because the Sensor API is flaky, the `curl` command inside the script uses retries. However, when a partial download fails and retries, the script blind-appends or re-processes duplicate records. You must ensure exact deduplication (each unique timestamp should only be processed once).
2. **Missing Resampling & Gap-Filling**: The upstream data arrives at irregular intervals (e.g., `10:01:15`, `10:01:54`). The downstream warehouse requires data resampled to strictly **1-minute intervals** (e.g., `10:01:00`, `10:02:00`). For any given minute, take the *first* record that occurred in that minute. If a minute has no records, you must insert a gap-fill record with the message `"GAP_DETECTED"`. The time window to process is exactly from `2024-01-01T12:00:00Z` to `2024-01-01T12:59:00Z` (inclusive).
3. **Multi-language Validation Flaw**: There is a validation checkpoint that drops messages exceeding 15 characters in length. The current Bash script calculates string length using byte count (`wc -c`), which incorrectly drops perfectly valid multi-byte Unicode strings (e.g., Japanese or Arabic logs). You must fix this quality gate to count actual *Unicode characters*.

**Your goal:**
Modify `/home/user/etl_pipeline.sh` so that when executed, it successfully extracts the data, deduplicates it, resamples/gap-fills it into 60 exact 1-minute buckets, validates the character limits correctly, and POSTs the final dataset to the Data Warehouse.

Once you have fixed and run the script, the Data Warehouse will calculate an accuracy score based on the ingested records. You must achieve a pipeline accuracy of at least 0.95 (95%).