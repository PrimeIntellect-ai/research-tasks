You are a data analyst investigating an incident. You have been provided with a video file `/app/incident_log.mp4` which contains a hidden subtitle track (SRT format) that periodically flashes CSV data representing a snapshot of our system's dependency graph and resource metrics.

Your task consists of two parts:

Part 1: Data Extraction
1. Extract the subtitle track from `/app/incident_log.mp4`.
2. Clean the extracted subtitles to reconstruct the original CSV data. The CSV will have the header `node_id,parent_id,metric_value`. 
3. Save this extracted CSV to `/home/user/extracted_graph.csv`.

Part 2: Hierarchical Aggregation Script
Write a standalone Bash script at `/home/user/aggregate_graph.sh` that takes a path to a CSV file (formatted exactly like the one you extracted) as its first and only argument. The script must parse this hierarchical data and calculate the total aggregated `metric_value` for every node. 

A node's total aggregated metric is defined as its own `metric_value` PLUS the aggregated metric of all its direct and indirect descendants (a recursive summation).

Requirements for `/home/user/aggregate_graph.sh`:
- It must be written primarily in Bash (using standard tools like `awk`, `jq`, `sed`, `grep`, etc. are perfectly fine and encouraged).
- The input CSV will have `node_id`, `parent_id`, and `metric_value`.
- A `parent_id` that is empty or equals `0` indicates a root node.
- The script must print the results to standard output in exactly the following CSV format (including the header):
  `node_id,total_metric`
- The output rows must be sorted numerically by `node_id` in ascending order.
- The script must handle graphs of arbitrary depth (up to 50 levels deep) and ignore circular dependencies (assume the input is always a valid directed acyclic graph/tree).

We will verify your solution by fuzzing your `/home/user/aggregate_graph.sh` against thousands of dynamically generated CSV test cases to ensure your recursive aggregation logic is strictly identical to our reference implementation.