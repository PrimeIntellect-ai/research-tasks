You are a data engineer tasked with building a high-performance ETL pipeline for a smart grid system. We have high-frequency power meter readings arriving as multiple JSONL files, and a metadata registry in CSV format mapping meters to grid regions. 

Your goal is to write a Rust application that processes this data in parallel, applies data cleaning and standardization, and aggregates the time series data by region.

**Input Data:**
1. **Metadata Registry:** `/home/user/data/metadata.csv`
   Columns: `meter_id,region_id`
   Example: `M001,North_Region`

2. **Time Series Readings:** `/home/user/data/readings_*.jsonl` (Multiple files)
   Format: JSON Lines
   Schema: `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "meter_id": "string", "reading_kw": float}`

**ETL Pipeline Requirements:**
Create a Rust project in `/home/user/etl_pipeline` and write a program that performs the following steps. You may use external crates like `serde`, `serde_json`, `csv`, `chrono`, and `rayon` (strongly recommended for parallel processing).

1. **Parallel Load & Hash-Based Deduplication:** 
   Read all `readings_*.jsonl` files. Due to sensor glitches, there may be duplicate readings for the exact same `meter_id` and `timestamp`. Deduplicate them using a hash-based approach. If duplicates exist, keep the record with the **maximum** `reading_kw` value.

2. **Join & Filter:**
   Join the deduplicated readings with `metadata.csv` to attach the `region_id`. Drop any readings for `meter_id`s that do not exist in the metadata registry.

3. **Normalization (Standardization):**
   For each individual `meter_id`, calculate the mean ($\mu$) and population standard deviation ($\sigma$) of its `reading_kw` across all its valid time series points.
   Standardize each reading into a Z-score: $z = (reading\_kw - \mu) / \sigma$. 
   *(Note: If $\sigma = 0$ or if a meter has only one reading, set $z = 0.0$ for those readings).*

4. **Time Series Grouping & Sorting:**
   Truncate the `timestamp` of each reading to the start of its hour (e.g., `2023-10-01T14:45:30Z` becomes `2023-10-01T14:00:00Z`). 
   Group the standardized records by `region_id` and the truncated `hour`. Calculate the sum of the Z-scores for each region-hour bucket.

**Output Requirements:**
The Rust program must output the final aggregated data to `/home/user/output/regional_load.csv`.
The output must have the following exact headers: `region_id,hour,sum_z_score`
The rows must be sorted alphabetically by `region_id` ascending, and then by `hour` chronologically ascending. Formatted to 4 decimal places for `sum_z_score`.

Write a bash script at `/home/user/run_etl.sh` that compiles the Rust project in release mode and executes it. Make sure the script is executable.