You are an automation specialist creating a data processing workflow. We have a pipeline that ingests system logs, but the upstream systems are messy. We need to process a JSON-Lines file, clean up character encodings, compute statistics, and write out a standardized CSV format.

Your task is to write a Rust application that processes this data. 

**Requirements:**

1. **Input Data**: Read the file at `/home/user/data/raw_metrics.jsonl`.
   Each line is a JSON object with the following schema:
   `{"id": "<string>", "timestamp": <integer>, "measurement": <float>}`

2. **Character Encoding & Normalization**:
   The `id` field contains raw string data that may include literal Unicode escape sequences (e.g., `\uFF21`). 
   - You must parse/unescape these literal Unicode escape sequences into their actual characters.
   - You must then normalize the resulting string using Unicode Normalization Form KC (NFKC).

3. **Parallel Data Processing**:
   You must use parallel processing (e.g., using the `rayon` crate) to parse the JSON lines and perform the initial unescaping and normalization steps concurrently.

4. **Rolling Statistics**:
   After normalizing the IDs, you need to group the records by the normalized `id`. 
   For each group, sort the records chronologically by `timestamp` (ascending). 
   Then, compute a 3-measurement Simple Moving Average (SMA) of the `measurement` field. 
   - For the 1st record in a group, the SMA is just its measurement.
   - For the 2nd record, the SMA is the average of the 1st and 2nd measurements.
   - For the 3rd record and beyond, the SMA is the average of the current measurement and the two immediately preceding measurements.

5. **Output**:
   Write the results to a CSV file at `/home/user/data/normalized_metrics.csv`.
   - The CSV must have the following exact header row: `normalized_id,timestamp,measurement,rolling_sma`
   - The rows must be sorted primarily by `normalized_id` (alphabetically) and secondarily by `timestamp` (ascending).
   - Format the `measurement` and `rolling_sma` to exactly 2 decimal places.

**Environment details**:
- Rust and Cargo are installed. 
- You may create your Rust project inside `/home/user/metrics_processor`.
- Once your Rust code runs and successfully produces the expected CSV at `/home/user/data/normalized_metrics.csv`, the task is complete.