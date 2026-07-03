You are a log analyst investigating patterns across multiple server clusters. Different clusters output logs in different formats, and due to intermittent monitoring failures, some metric data points are missing.

Your task is to build a Python pipeline that reads these multi-format logs, unifies them, imputes missing values based on time-series rules, and writes the results. To ensure scalability, you must implement a lightweight Directed Acyclic Graph (DAG) task runner within your script to orchestrate the pipeline stages.

**Input Data:**
There are two log files in `/home/user/raw_logs/`:
1. `cluster_a.csv`: Contains logs from Cluster A in CSV format (`timestamp`, `cpu_usage`, `memory_usage`).
2. `cluster_b.json`: Contains logs from Cluster B as a JSON array of objects (keys: `t`, `cpu`, `mem`).

**Data Processing Rules:**
1. **Unification:** Combine the records from both files into a single dataset.
2. **Sorting:** Sort the combined dataset chronologically by the timestamp (which is an integer representing seconds).
3. **Imputation:** 
   - Some `cpu_usage` (or `cpu`) values are missing (empty strings in CSV, `null` in JSON). Fill these using **linear interpolation** with respect to the timestamp between the nearest prior and subsequent known `cpu` values. 
   - Some `memory_usage` (or `mem`) values are missing. Fill these using **forward fill** (use the most recent known chronological memory value). You can assume the very first record chronologically will always have a valid memory value.
4. **Format normalization:** The final unified dataset must standardize the keys as: `timestamp`, `cpu`, `memory`.

**DAG Orchestration Requirement:**
You must implement a simple DAG executor in your Python script (`/home/user/pipeline.py`). 
- The DAG must represent tasks as functions and dependencies.
- You must define at least these distinct tasks: `extract_a`, `extract_b`, `transform_impute` (depends on both extractions), and `load_results` (depends on transform).
- The executor must automatically resolve the execution order based on dependencies and run them.
- During execution, the executor must append the name of each task as it finishes to `/home/user/dag_trace.txt` (one task name per line).

**Outputs:**
1. Write the DAG pipeline script to `/home/user/pipeline.py`.
2. Run your script to generate `/home/user/unified.jsonl`, where each line is a valid JSON object of a unified, imputed log record.
3. Your script must generate the `/home/user/dag_trace.txt` file proving the DAG execution order.

Make sure the output JSONL file contains exactly `timestamp` (int), `cpu` (float, 1 decimal place), and `memory` (int) keys.