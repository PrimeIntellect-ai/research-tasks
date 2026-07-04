You are acting as a log analyst and data engineer investigating an issue with our ETL pipeline. 

Our upstream log generator (Service A) occasionally experiences network drops and retries sending batches of logs, resulting in exact duplicate records. We use Redis as an intermediate buffer queue.

Your task is to write a high-performance C++ ETL consumer (`/home/user/etl_worker.cpp`) that reads these logs, processes them, and writes the clean results to disk.

There are currently two services running:
1. **Redis**: Running on `localhost:6379`.
2. **Log Generator**: A Python service on `localhost:5000`. You can trigger it to push a batch of logs into Redis by running `curl -X POST http://localhost:5000/start`. It pushes JSON strings to a Redis list key called `raw_logs`.

Each raw log is a JSON object with the following format:
`{"log_id": "a1b2c3d4...", "level": "INFO", "service_code": "SVC01", "message": "User Logged IN!!"}`

You must implement the C++ processor with the following pipeline requirements:
1. **Large-file/Stream Handling**: Pop items continuously from the `raw_logs` Redis list. Wait/block if empty, but exit gracefully if the list is empty and no new logs have arrived for 3 seconds.
2. **Deduplication**: The generator sends duplicates due to retry logic. You must drop any log whose `log_id` you have already seen. Keep only the first occurrence.
3. **Normalization**: Tokenize and normalize the `message` field. Convert it to entirely lowercase. Replace any non-alphanumeric character (anything that is not `a-z`, `0-9`) with a single space. Collapse multiple consecutive spaces into a single space, and strip leading/trailing spaces.
4. **Join**: Read a metadata file located at `/home/user/service_map.csv` (format: `service_code,service_name`). Add a `service_name` field to the JSON. If a `service_code` is not found, set `service_name` to `"UNKNOWN"`.
5. **Stratification / Sampling**: We want to keep 100% of `"ERROR"` and `"WARN"` logs. However, for `"INFO"` logs, we only want a deterministic 10% sample to save space. A log with level `"INFO"` should only be kept if the integer parsed from the first 4 characters of its `log_id` (parsed as a hexadecimal number) modulo 10 equals 0. For example, if `log_id` starts with `"1a2f"`, parse `"1a2f"` as hex (6703), and since `6703 % 10 == 3 != 0`, drop it.
6. **Output**: Write the remaining logs as single-line JSON strings to `/home/user/processed_logs.jsonl`. The output JSON keys must be: `log_id`, `level`, `service_code`, `service_name`, `message`.

**Compilation and execution**:
You have `libhiredis-dev` and `nlohmann-json3-dev` installed.
Compile your code using: `g++ -O3 etl_worker.cpp -lhiredis -o etl_worker`
You should start your worker, then trigger the generator (`curl -X POST http://localhost:5000/start`), and wait for your worker to finish.

**Verification**:
An automated grading script will evaluate `/home/user/processed_logs.jsonl`. Because order might slightly vary and C++ JSON serializers might order keys differently, the verifier will parse both your output and our secret reference file, calculating the Jaccard similarity between the sets of processed log objects. You must achieve a Jaccard similarity score >= 0.99.