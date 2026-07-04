You are an automation specialist working on building robust ETL workflows. We have a legacy, compiled ETL worker binary located at `/app/etl_worker`. It simulates pulling data from various upstream sources and streams it to standard output. 

Unfortunately, this binary has a bug: it often simulates "retries" that produce duplicate records, and occasionally the upstream data source experiences a severe sensor calibration error (a changepoint) causing all numerical values to suddenly multiply by a massive factor.

Your task is to write a Python script `/home/user/pipeline.py` that handles this messy data stream.

Requirements:
1. **Data Generation**: Your script should execute `/app/etl_worker 50000` and capture its standard output.
2. **Parsing**: The output consists of log lines formatted as: `ID|TIMESTAMP|FORMAT|PAYLOAD`. 
   - `FORMAT` can be `JSON`, `CSV`, or `XML`. 
   - `PAYLOAD` contains the actual data representing three fields: `id` (int), `category` (string: A, B, or C), and `value` (float). 
   - You must construct regex patterns to parse the log lines and extract the payload, then use multi-format parsing to extract `id`, `category`, and `value`.
3. **Deduplication**: The ETL job produces duplicate records (same `id`). You must keep only the chronologically *first* occurrence of each `id` based on the `TIMESTAMP`.
4. **Changepoint/Anomaly Detection**: At some point in the stream, the `value` field for all new records suddenly jumps by an order of magnitude (the changepoint). You must detect this changepoint and discard all records that occur *after* the changepoint begins.
5. **Stratified Sampling**: From the remaining clean, deduplicated records, take a 20% random sample stratified by the `category` field. Use a random seed of `42` for reproducibility.
6. **Output**: Write the final sampled records to `/home/user/cleaned_sample.json` as a JSON array of objects, where each object has `id`, `category`, and `value`.

Ensure your Python script is robust and executable. Do not modify the binary. We will evaluate your resulting `/home/user/cleaned_sample.json` against a ground-truth reference dataset.