You are a data engineer building an ETL pipeline to analyze an enterprise transaction graph. 

Part of the pipeline's configuration was provided as a screenshot of an old dashboard, located at `/app/config_rules.png`. You must extract the filtering thresholds from this image (e.g., using `tesseract`). The image contains exactly three lines of text specifying key-value pairs separated by an equals sign (e.g., `KEY=VALUE`). 

Your main objective is to write a Python script at `/home/user/process_graph.py` that processes a stream of incoming transaction data representing graph edges, applies the rules from the image, aggregates the node metrics, and outputs the final result.

Script Specifications:
1. **Input:** The script must read a single JSON array from Standard Input (`stdin`). Each element in the array is an object representing a directed edge: `{"src": "node_id", "dst": "node_id", "type": "edge_type", "weight": integer}`.
2. **Filtering Rules (from OCR):**
   - Discard any edges where the `type` matches the `EXCLUDE_TYPE` from the image.
   - Discard any edges where the `weight` is strictly greater than the `MAX_WEIGHT` from the image.
3. **Aggregation:** Treat the remaining edges as an undirected graph. For each distinct node present in the filtered edges, calculate:
   - `degree`: The total number of incident edges (in-degree + out-degree).
   - `weight_sum`: The sum of the weights of all incident edges.
4. **Post-Aggregation Filtering:** Discard any nodes whose `degree` is strictly less than the `MINIMUM_DEGREE` extracted from the image.
5. **Output Format:** The script must print a single JSON array to Standard Output (`stdout`), containing objects of the form `{"node": "node_id", "degree": integer, "weight_sum": integer}`.
6. **Sorting:** The output JSON array must be sorted by `degree` in descending order. If degrees are equal, sort by `node` ID in ascending alphabetical order.

The script must be robust and handle empty inputs or inputs where no nodes meet the criteria (outputting an empty array `[]` in such cases). Do not print anything else to `stdout` except the final JSON output.