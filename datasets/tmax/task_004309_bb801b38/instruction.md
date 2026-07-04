You are acting as a data scientist analyzing molecular graphs. Your pipeline receives molecular interaction networks, but the data feed is polluted with randomly generated "adversarial" graphs that do not represent real chemistry.

You have a multi-service pipeline located in `/home/user/pipeline/`. It consists of:
1. A Redis server (acting as a task queue).
2. A Python API (`/home/user/pipeline/api.py`) that receives graph payloads via HTTP POST, and pushes them to a Redis list `graph_queue`.
3. A Rust worker (`/home/user/pipeline/rust_worker/`) that pops tasks from Redis, processes them, and outputs the result.

Your objectives:

1. **Service Composition**: 
   Create a bash script at `/home/user/start_services.sh` that starts the Redis server (default port 6379), the Python API (port 5000), and the Rust worker in the background. Ensure they can communicate (you may need to configure environment variables like `REDIS_URL="redis://localhost:6379"`).

2. **Graph Analysis & Parallelization (Rust)**:
   Modify the Rust worker to classify graphs as either "clean" (real molecules) or "evil" (random noise). You must process the graph nodes in parallel using the `rayon` crate.
   - A graph is given as a JSON object with `nodes` (list of IDs) and `edges` (list of `[u, v]` pairs).
   - Implement the calculation of the **Average Clustering Coefficient** and **Maximum Node Degree**.
   - Use the following statistical/domain rule: Real molecular graphs have a `max_degree` $\le 4$ and an `avg_clustering_coefficient` $> 0.0$. Random "evil" graphs in our dataset violate these properties (either high degree or zero clustering).

3. **Adversarial Corpus Verification**:
   The Rust worker must write a file `/home/user/classification_results.csv` with lines formatted as: `graph_id,status`, where `status` is either `CLEAN` or `EVIL`. 
   For testing your logic, there are two corpora of raw JSON graphs provided in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`. 

Ensure your Rust worker compiles successfully via `cargo build --release`. The automated verifier will start your services using `/home/user/start_services.sh`, send the contents of the `clean` and `evil` corpora to the API on port 5000, and evaluate `/home/user/classification_results.csv`.