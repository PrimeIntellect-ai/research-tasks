You are a localization engineer managing translation event logs. Recently, an upstream ETL job crashed and retried, dumping duplicate records into your ingestion file. Furthermore, the logs contain raw user IP addresses which must be anonymized before they can be loaded into the data warehouse.

Your task is to write a standalone Rust script (`/home/user/etl_fix.rs`) to process the raw CSV data into a clean, aggregated summary.

**Input Data:**
The file `/home/user/raw_loc_events.csv` contains the translation events. 
The CSV has a header: `ts,ip,loc_key,conf`
- `ts`: Unix timestamp in seconds (integer).
- `ip`: IPv4 address of the translator.
- `loc_key`: The string identifier being translated.
- `conf`: The translation confidence score (integer).

**Requirements for your Rust script:**
1. **Deduplication:** The ETL retry caused exact duplicate rows. Ignore the header, and deduplicate identical lines before processing.
2. **Data Masking:** Anonymize the `ip` by replacing the last octet (everything after the last `.`) with `0`. (e.g., `192.168.1.55` becomes `192.168.1.0`).
3. **Time-based Bucketing:** Group the events by an `hour_bucket`. Calculate this by flooring the `ts` to the nearest multiple of 3600.
4. **Aggregation:** For each `(hour_bucket, loc_key)` group, calculate:
   - The number of **unique** masked IPs.
   - The average `conf` score (integer division, round down to the nearest whole number).
5. **Output:** Write the results to `/home/user/loc_summary.csv`. The output must have the header `hour_bucket,loc_key,unique_masked_ips,avg_conf` and be sorted in ascending order first by `hour_bucket`, then alphabetically by `loc_key`.

You must only use the Rust standard library (no external crates). Compile your script using `rustc /home/user/etl_fix.rs` and execute it to generate the final CSV.