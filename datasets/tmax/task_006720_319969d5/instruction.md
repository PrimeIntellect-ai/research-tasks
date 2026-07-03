You are a log analyst investigating performance patterns across a cluster of legacy and modern servers. You have received heterogeneous log files, but they are messy, in different formats, and use different encodings. 

Your task is to build a data processing pipeline using **C++** and bash orchestration to clean, reshape, and extract anomaly features from these logs.

### Input Data
You will find two log files in `/home/user/inputs/`:
1. **`/home/user/inputs/cpu_metrics.csv`**: A CSV file containing CPU usage logs. 
   - **Format**: Wide-format CSV. Columns: `timestamp,srv_alpha,srv_beta,srv_gamma`
   - **Encoding**: UTF-16LE (Due to a legacy Windows logging system).
   - **Example row**: `1622505600,45.2,88.5,32.1`

2. **`/home/user/inputs/mem_metrics.json`**: A JSON file containing Memory usage logs.
   - **Format**: An array of JSON objects. Keys are `ts` (timestamp), `srv_alpha`, `srv_beta`, `srv_gamma`.
   - **Encoding**: UTF-8.
   - **Example row**: `[{"ts": 1622505600, "srv_alpha": 60.5, "srv_beta": 91.2, "srv_gamma": 40.0}, ...]`

### Requirements
1. **Pipeline Orchestration (`/home/user/run_pipeline.sh`)**:
   Create a bash script named `run_pipeline.sh` that orchestrates the entire workflow. It must:
   - Handle the character encoding conversion of the CSV file to UTF-8.
   - Compile the C++ program (using `g++ -std=c++17`).
   - Execute the C++ program to process the data.

2. **C++ Data Processor (`/home/user/processor.cpp`)**:
   Write a C++ program that reads the UTF-8 converted CSV and the JSON file, and performs the following:
   - **Reshaping**: Convert both datasets from "wide" format to a unified "long" format. A single long-format record represents one server, one metric type (`cpu` or `mem`), at one timestamp.
   - **Feature Extraction**: Evaluate an `is_anomalous` boolean feature for each long-format record. Anomaly conditions:
     - CPU usage > 85.0
     - Memory usage > 90.0
   - **Filtering**: Drop all non-anomalous records. Keep *only* records where `is_anomalous` is true.
   - **Sorting**: Sort the anomalous records chronologically by `timestamp` (ascending). If timestamps are equal, sort by `server` name (alphabetically ascending). If server names are equal, sort by `metric` name (alphabetically ascending).

3. **Output File (`/home/user/output/anomalies.jsonl`)**:
   The C++ program must write the results to `/home/user/output/anomalies.jsonl` in JSON Lines format (one valid JSON object per line).
   - Schema per line: `{"timestamp": <int>, "server": "<string>", "metric": "<string>", "value": <float>}`
   - Ensure floats are printed to 1 decimal place.

Make sure `/home/user/run_pipeline.sh` is executable and creates the `/home/user/output/` directory if it does not exist.