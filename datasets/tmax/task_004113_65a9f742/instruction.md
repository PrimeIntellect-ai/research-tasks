You are a data engineer managing an ETL pipeline written in C. The current pipeline processes a stream of multi-lingual text records (in JSON format) from a local HTTP source, extracts specific fields, computes some summary statistics, and stores the processed records. However, the system has a bug: when the data source experiences intermittent connection issues, our naive retry logic kicks in and causes duplicate records to be processed and stored. 

We need you to implement a robust, hash-based deduplication mechanism in the C ETL processor, ensure proper Unicode text processing, compute accurate summary statistics, and expose a simple HTTP endpoint for monitoring.

Here is the setup:
1. Under `/app/services/` there is a `docker-compose.yml` (simulated via local background scripts) that starts:
   - A mock upstream data source on `localhost:8081` that serves JSON records. It is intentionally flaky and sometimes drops connections, triggering retries in the ETL client.
   - A Redis instance on `localhost:6379` for caching/state management.
2. Your ETL worker code is located in `/home/user/etl_worker/`. It currently fetches data from `localhost:8081/stream`, processes it, and writes the output to `/home/user/etl_worker/output.jsonl`.
3. The records from the upstream source have the format: `{"id": "<uuid>", "text": "<multi-language utf-8 text>", "category": "<string>", "value": <float>}`.

Your tasks:
1. **Deduplication:** Modify the C ETL worker (`/home/user/etl_worker/worker.c`) to compute an MD5 or SHA-1 hash of the `id` field for each record. Use Redis to track seen hashes and drop duplicate records.
2. **Data Processing & Aggregation:** Ensure that the text field is properly parsed as UTF-8. Calculate the total number of unique records processed, the average of the `value` field per `category`, and extract a 10% stratified sample (based on category) of the unique records.
3. **Monitoring Endpoint:** The C program must also listen on TCP port `9090` (HTTP). When an HTTP GET request is made to `http://localhost:9090/stats`, it must return a JSON response containing:
   - `total_unique`: Integer
   - `averages`: A dictionary mapping each category to its average value.
   - `sample_count`: The number of records in the 10% sample.
4. **Build and Run:** Use the provided Makefile in `/home/user/etl_worker/` to build the worker. Run it and ensure it processes at least 1000 records from the upstream source.

Write the deduplicated records (including the 10% sample flagged with a `"sampled": true` field) to `/home/user/etl_worker/output_clean.jsonl`. The final format of this file must be valid JSON Lines.

You must rely strictly on standard bash utilities and the C compiler (`gcc`). The worker should run as a daemon or background process so the verification scripts can query port 9090.