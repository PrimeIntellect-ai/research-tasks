You are tasked with building a configuration change tracking pipeline. You have been provided with several JSONL files in `/home/user/data/` containing configuration snapshots of various servers over time.

Each line in the files is a JSON object with the following schema:
`{"server_id": "server_X", "timestamp": 1600000000, "config": {"setting1": "A", "setting2": "B", ...}}`

Your objective is to analyze the configuration drift for each server using parallel processing, calculate the similarity between consecutive configurations, and find anomalies using a rolling statistic.

Perform the following steps:

1. Write a Python script `/home/user/config_analyzer.py` that processes the data. 
   - It must read all `.jsonl` files in `/home/user/data/`.
   - Group the records by `server_id` and sort them chronologically by `timestamp`.
   - For each server, compute the **Jaccard similarity** between consecutive configuration snapshots (i.e., between state at $t_{i}$ and state at $t_{i+1}$). A configuration is treated as a set of `"key=value"` strings.
     - Jaccard similarity = (size of intersection) / (size of union).
   - Compute a **rolling average** of the Jaccard similarity over a window of the last 3 changes (including the current change). If there are fewer than 3 changes available, average the available ones.
   - Use Python's `multiprocessing` module to process different `server_id`s in parallel.
   - The script must output a CSV file to `/home/user/results.csv` with the header `server_id,timestamp,similarity,rolling_avg`. 
     - The `timestamp` is the timestamp of the *later* snapshot ($t_{i+1}$).
     - Output `similarity` and `rolling_avg` formatted to exactly 4 decimal places.
     - Sort the output CSV ascendingly by `server_id`, then by `timestamp`.

2. After running your Python script, use standard bash commands (like `awk`) to filter `/home/user/results.csv`. Extract all rows where `rolling_avg` is strictly less than 0.5000 and save them to `/home/user/alerts.csv`. This file should also include the header.

Ensure your Python script runs efficiently and handles the multi-stage logic as described.