You are a data engineer tasked with building an algorithmic ETL pipeline to process and analyze noisy sensor logs. You need to write a Go program that processes two datasets, cleans the data, and calculates similarity metrics to detect repeated but slightly garbled error messages.

You are provided with two files:
1. `/home/user/raw_logs.csv`: A CSV file containing noisy log events.
   Columns: `log_id,timestamp,sensor_id,message`
2. `/home/user/sensors.json`: A JSON file mapping sensors to their deployment regions.
   Format: `[{"sensor_id": "S1", "region": "North"}, ...]`

Your Go program must perform the following pipeline steps:

1. **Deduplication**: Hash or group the records from `raw_logs.csv` to find unique messages per `sensor_id`. If a `sensor_id` produces the exact same `message` multiple times, keep only one instance of that message for that sensor.
2. **Join**: Associate each deduplicated message with its `region` by joining with `sensors.json` on `sensor_id`. If a `sensor_id` is not found in the JSON, ignore those logs.
3. **Similarity Computation**: Group the deduplicated messages by `region`. For each region, compute the Levenshtein distance (character-level edit distance) between all unique pairs of messages within that region. 
4. **Aggregation & Sorting**: For each region, calculate:
   - `unique_message_count`: The total number of unique messages in this region (across all valid sensors in it).
   - `min_levenshtein_distance`: The minimum Levenshtein distance found between any two *distinct* messages in this region. If a region has fewer than 2 unique messages, set this to `-1`.
5. **Output**: Write the aggregated results to a CSV file at `/home/user/region_stats.csv`. 
   The CSV must have the exact headers: `region,unique_message_count,min_levenshtein_distance`.
   The rows must be sorted alphabetically by `region` in ascending order.

Write your Go code in `/home/user/etl.go`, compile it, and run it to produce the final `region_stats.csv`. You may use standard Go library packages only.