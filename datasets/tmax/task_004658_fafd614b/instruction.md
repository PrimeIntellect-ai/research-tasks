You are a log analyst investigating server performance patterns associated with user access. You need to build a data processing pipeline in Python to analyze raw telemetry and access logs.

Your task is to create a Python script at `/home/user/pipeline.py` that acts as a Directed Acyclic Graph (DAG) orchestrator to process these logs. You may install and use external libraries like `pandas` and `networkx`.

Here are the details of the pipeline you need to implement:

**1. Inputs:**
You are provided with two files:
*   `/home/user/telemetry.csv`: Contains `timestamp` (integer), `server_id` (string), `cpu_usage` (float), and `memory_usage` (float). Some `cpu_usage` and `memory_usage` values are missing (empty strings).
*   `/home/user/access.csv`: Contains `timestamp` (integer), `server_id` (string), `user_email` (string), and `user_ip` (string).

**2. DAG Nodes & Operations:**
Your pipeline must define and execute the following nodes in a valid topological order based on their dependencies:
*   **`Extract_Telemetry`**: Reads `/home/user/telemetry.csv`.
*   **`Extract_Access`**: Reads `/home/user/access.csv`.
*   **`Impute_Telemetry`** (Depends on `Extract_Telemetry`): Fills missing `cpu_usage` and `memory_usage` values using linear interpolation. The interpolation must be performed per `server_id`, ordered by `timestamp`. If leading/trailing values are missing, use forward/backward fill after interpolation.
*   **`Mask_Access`** (Depends on `Extract_Access`): Anonymizes PII. Replace `user_email` with its lowercase SHA-256 hex digest. Mask `user_ip` by replacing the last octet with `0` (e.g., `192.168.1.45` becomes `192.168.1.0`).
*   **`Merge_And_Aggregate`** (Depends on `Impute_Telemetry` and `Mask_Access`): Performs an inner join of the imputed telemetry and masked access data on `timestamp` and `server_id`. Then, group by `user_ip` (the masked version) and calculate the mean `cpu_usage` and mean `memory_usage`. Round the means to 2 decimal places.
*   **`Load`** (Depends on `Merge_And_Aggregate`): Saves the final aggregated DataFrame to `/home/user/processed_logs.csv`. The CSV should have columns `user_ip`, `cpu_usage`, `memory_usage` and be sorted alphabetically by `user_ip`.

**3. Pipeline Logging & Orchestration:**
The pipeline must track its execution. Write logs to `/home/user/pipeline.log`.
Whenever a node starts or completes, append a line exactly matching this format:
`[INFO] - Node {node_name} started.`
`[INFO] - Node {node_name} completed.`
The nodes must only execute after their dependencies have successfully completed.

Write and execute the `/home/user/pipeline.py` script to produce the final `processed_logs.csv` and `pipeline.log`.