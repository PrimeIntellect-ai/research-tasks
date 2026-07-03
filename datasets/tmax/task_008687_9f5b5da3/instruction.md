You are a data analyst troubleshooting an ETL pipeline. A buggy pipeline retry mechanism has produced a raw CSV file at `/home/user/sensor_data.csv` containing duplicate records for the same sensor at the same timestamp. 

You need to write and execute a Rust program to clean this data, compute windowed statistics, and generate a formatted text report. 

Here are the requirements:
1. Read `/home/user/sensor_data.csv`. The file has the header: `timestamp,sensor_id,value`.
2. **Deduplication / Summary Stats**: For any given `sensor_id` and `timestamp`, combine duplicate records by taking the *average* (arithmetic mean) of their `value`s.
3. **Rolling Aggregation**: For each `sensor_id`, order the deduplicated records chronologically by `timestamp` (ascending). Compute a 3-period simple moving average (SMA) of the values. 
   - If fewer than 3 periods are available for a given timestamp's window, compute the average of the available periods (e.g., the first period's SMA is just its own value; the second period's SMA is the average of the first two).
4. **Template Generation**: For each `sensor_id` (in alphabetical order), determine the *maximum* moving average reached at any point, and the *final* moving average (the SMA at the latest timestamp for that sensor). 
   Output these results to `/home/user/report.txt` exactly following this template format:

```
Sensor {sensor_id}:
- Max 3-Period SMA: {max_sma}
- Final 3-Period SMA: {final_sma}

```
(Note the blank line after each sensor block).

Format the `{max_sma}` and `{final_sma}` strictly to 2 decimal places (e.g., `55.00`, `22.67`).

You may use standard Rust commands (`cargo new`, etc.) to build and run your solution. Standard library is sufficient, but you may use external crates if you set up the `Cargo.toml` appropriately.