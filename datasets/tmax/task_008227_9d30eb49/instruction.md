You are a data scientist cleaning a corrupted dataset of system logs. You need to build a robust ETL pipeline in Rust that interacts with a local embedding service, performs dimensionality reduction to identify anomalous logs, and filters the dataset.

**Setup Instructions:**
1. There is a Python-based embedding API located at `/home/user/service/embed_app.py`. It requires `flask`. Install any necessary Python dependencies and start this service as a background process. It binds to `127.0.0.1:8080`.
2. The raw dataset is located at `/home/user/data/logs.csv`. It has two columns: `id` (integer) and `text` (string).

**Rust ETL Pipeline Requirements:**
Create a Rust project in `/home/user/etl_cleaner` that does the following:
1. **Extract**: Read the `logs.csv` dataset.
2. **Embed**: For each row, query the local API at `http://127.0.0.1:8080/embed` via a POST request. 
   - Payload format: `{"text": "<log_text>"}`
   - Response format: `{"embedding": [float; 10]}` (a 10-dimensional vector).
3. **Dimensionality Reduction**: Project the 10-dimensional embedding down to 2 dimensions (X, Y) using the following linear transformation (matrix multiplication):
   - `X = sum(embedding[i] * R1[i])` for i in 0..10
   - `Y = sum(embedding[i] * R2[i])` for i in 0..10
   - Where `R1 = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
   - Where `R2 = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]`
4. **Clean**: Calculate the Euclidean distance of the resulting 2D vector `(X, Y)` from the origin `(0.0, 0.0)`. Anomaly threshold: If the distance is strictly greater than `15.0`, the log is considered an anomaly and must be discarded.
5. **Load**: Write the `id`s of the *valid* (non-anomalous) logs to `/home/user/valid_logs.txt`. 
   - The file should contain one `id` per line.
   - The `id`s must be sorted in ascending order.

Ensure your Rust project compiles and successfully creates the `/home/user/valid_logs.txt` file based on the full CSV.