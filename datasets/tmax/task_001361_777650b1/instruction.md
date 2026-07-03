I need you to build a high-performance C++ configuration tracking pipeline. We are processing massive streams of server configuration changes, and we need to detect "configuration storms" (servers experiencing unusually high rates of changes) using rolling window aggregations.

Here is the full workflow you need to implement:

1. **Fix and Install the Vendored JSON Parser:**
   We are using `simdjson` for high-speed parsing. I have vendored the source code of `simdjson` v3.6.0 at `/app/simdjson`. Unfortunately, someone modified its `CMakeLists.txt` to test legacy compiler support, and now it fails to build. You must find the deliberate perturbation (hint: it's related to the C++ standard required by simdjson), fix it, and build/install the library locally so your C++ program can link against it. 

2. **Data Ingestion and Joins:**
   You will find two datasets in `/home/user/data/` (you will need to assume they exist and are populated during testing):
   * `server_meta.csv`: Contains metadata for each server. Format: `server_id,tier,max_changes_per_min` (e.g., `srv-01,frontend,50`).
   * `config_changes.jsonl`: A massive stream of JSON lines. Format: `{"timestamp": 1700000000, "server_id": "srv-01", "config_key": "nginx_workers", "new_value": "16"}`. 

3. **Validation Checkpoints (Quality Gates):**
   Your pipeline must drop (ignore) any JSON line that fails these checks:
   * Missing `timestamp`, `server_id`, or `config_key`.
   * `timestamp` is strictly less than `1700000000`.
   * `server_id` does not exist in `server_meta.csv`.

4. **Rolling Aggregation:**
   For all valid records, compute the total number of configuration changes per `server_id` in **60-second tumbling windows**.
   * A tumbling window is defined strictly by the Unix `timestamp` divided by 60. For example, `[1700000000, 1700000059]` is one window. The window start time is `(timestamp / 60) * 60`.

5. **Detection and Output:**
   If a server's change count in a single 60-second window *strictly exceeds* its `max_changes_per_min` (from the CSV join), flag it as a configuration storm.
   Write the flagged anomalies to `/home/user/output/anomalies.csv` with exactly this header and format:
   `server_id,window_start,change_count`
   *(e.g., `srv-01,1700000000,65`)*

**Requirements:**
* Write your solution in C++ 17 or higher. Place your code in `/home/user/src/config_tracker.cpp`.
* Compile it to an executable named `/home/user/bin/config_tracker`.
* Execute the program to generate the output file.
* You are evaluated on the **F1-score** of your output against a hidden ground-truth file. Your pipeline must achieve an F1-score of **>= 0.98** to pass.