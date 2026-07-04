You are a data engineer tasked with rewriting a critical but poorly optimized legacy ETL pipeline.

The legacy pipeline is provided as a compiled, stripped executable at `/app/legacy_etl`.
It reads a CSV from standard input with the following columns:
`timestamp, user_id, value`
(The timestamp is in ISO 8601 format, e.g., `2023-10-01T14:32:11Z`).

It outputs a processed CSV to standard output with the following columns:
`aligned_time, masked_user_id, anomaly_score`

The legacy tool performs timestamp alignment, data masking (anonymizing the user IDs), and calculates an anomaly score based on recent values. However, it is far too slow to handle our new streaming data volumes. 

Your task is to:
1. Reverse-engineer the basic logic of `/app/legacy_etl` by analyzing its input/output on sample data. You can generate sample data or use your own tests.
2. Write a highly optimized replacement program. You may use any language available in the environment (Python with pandas/numpy, Go, C++, etc.).
3. Create an executable entrypoint at `/home/user/fast_etl` (this can be your compiled binary, or a bash script that runs your Python/code) that reads from `stdin` and writes to `stdout` exactly like the legacy tool.

**Success Criteria:**
An automated verifier will test your `/home/user/fast_etl` against a hidden dataset of 500,000 rows.
- **Accuracy:** The Mean Squared Error (MSE) of your `anomaly_score` compared to the legacy tool's output must be less than `0.001`. The `aligned_time` and `masked_user_id` must match exactly.
- **Performance:** Your implementation must achieve at least a **5x speedup** in execution time compared to `/app/legacy_etl` on the hidden dataset.

You have full freedom in how you implement the data processing, as long as the output matches the legacy oracle's behavior.