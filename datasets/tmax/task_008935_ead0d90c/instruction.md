You are a data scientist cleaning a large sensor dataset. The data is currently stored in a large CSV file `/home/user/sensor_data.csv` containing two columns: `timestamp` (integer Unix seconds) and `value` (float). 

Because the real datasets are massive, you need to build a memory-efficient stream processor in Rust that aggregates this data into hourly buckets.

Please write a Rust program in a new Cargo project located at `/home/user/aggregator`. 
The program must:
1. Read the CSV data from `stdin` (streaming, do not load the whole file into memory at once).
2. Group the data into 1-hour time buckets. A bucket's starting timestamp is defined as `timestamp - (timestamp % 3600)`.
3. For each bucket, calculate the `mean` and `population variance` of the values. 
   - Mean = sum(values) / count
   - Population Variance = sum((x - mean)^2) / count
4. Log pipeline progress to `stderr` by printing exactly `Processed {N} records` every 50,000 records (i.e., at 50000, 100000, etc.).
5. When `stdin` reaches EOF, print the aggregated results to `stdout` in JSONL format, one JSON object per line, sorted by `hour_start` in ascending order.
   Format of each line:
   `{"hour_start": <integer>, "count": <integer>, "mean": <float>, "variance": <float>}`

Once your Rust tool is built, run it using the provided `/home/user/sensor_data.csv` via standard input, redirecting standard output to `/home/user/aggregated.jsonl` and standard error to `/home/user/pipeline.log`.

For example:
`cat /home/user/sensor_data.csv | cargo run --release > /home/user/aggregated.jsonl 2> /home/user/pipeline.log`