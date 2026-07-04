You are a data analyst responsible for building a real-time text anomaly detection pipeline. You need to implement a stream processing script and orchestrate the data flow between several local services.

### Part 1: Stream Processor (Anomaly Detection)
Write a script at `/home/user/analyzer.py` (you may use Python, Perl, or Ruby) that reads CSV data from standard input line-by-line and writes processed CSV data to standard output.

**Input format:** `event_id,timestamp,raw_text`
**Output format:** `event_id,token_count,anomaly_score`

**Processing Rules:**
1. **Normalization:** Extract the `raw_text` field. Convert it to lowercase. Replace any character that is not a letter (`a-z`), digit (`0-9`), or space (` `) with a space. Collapse multiple consecutive spaces into a single space. Strip leading and trailing spaces.
2. **Tokenization:** Count the number of space-separated words in the normalized text to get the `token_count`.
3. **Anomaly Detection (Changepoint):** Calculate an `anomaly_score` based on a rolling window of the **strictly previous 20** `token_count` values.
   - If fewer than 20 previous records have been processed in the stream, the `anomaly_score` is exactly `0.0000`.
   - Once 20 previous records exist, calculate the mean and the **population standard deviation** (divide by N=20, not N-1) of those 20 previous counts.
   - `anomaly_score = abs(current_token_count - mean) / std_dev`.
   - If `std_dev` is `0`, output `0.0000`.
   - Format the score to exactly 4 decimal places (e.g., `2.3450`).

*Note: Your script must process and output line-by-line in a streaming fashion, flushing standard output after each line.*

### Part 2: Pipeline Orchestration
We have a multi-service setup that you need to glue together.
1. **Redis** is running on `localhost:6379`.
2. An ingestion API at `/app/api_server.py` (which you must start) listens on port 5000. It accepts `POST /submit` requests with raw CSV lines and appends them to `/tmp/input_stream.csv`.
3. A forwarder script at `/app/redis_forwarder.py` (which you must start) tails a file named `/tmp/output_stream.csv` and pushes the lines to a Redis list named `anomalies`.

You must write a bash script at `/home/user/start_pipeline.sh` that:
- Starts the API server in the background.
- Starts a process that tails `/tmp/input_stream.csv` (following new lines), pipes it through your `/home/user/analyzer.py`, and appends the output to `/tmp/output_stream.csv`.
- Starts the Redis forwarder in the background.

Make sure your shell script sets up the files properly before tailing, and leaves the services running.