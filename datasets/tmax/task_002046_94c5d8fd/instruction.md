You are tasked with fixing and securing a data ingestion pipeline for an e-commerce platform. The pipeline processes CSV files containing product catalogs, but it has recently been targeted by malicious data injections, and its microservice architecture has become disconnected after a botched deployment.

Your goal is to complete two major objectives: write a robust data sanitizer, and reconfigure the multi-service pipeline to correctly route and process the cleaned data.

### 1. Data Sanitizer (Adversarial Filter)
You must write a Python script at `/home/user/data_pipeline/sanitizer.py` that reads an input CSV file and writes out a cleaned CSV file. 
The CSV files contain the following columns: `id` (integer), `parent_id` (integer or empty), `name` (string), `price` (float), `metadata` (JSON string).

Your `sanitizer.py` must be invoked exactly like this:
`python3 /home/user/data_pipeline/sanitizer.py <input_csv_path> <output_csv_path>`

It must drop any row that violates ANY of the following rules (preserving all valid rows):
1. **Valid Prices:** `price` must be greater than or equal to `0.0`.
2. **Valid Graph Relationships:** `id` cannot be equal to `parent_id` (this causes infinite loops in our recursive CTEs downstream).
3. **Valid JSON:** `metadata` must be a valid parseable JSON object/dict.
4. **No SQL Injection:** `name` must NOT contain the substrings `DROP TABLE` or `UNION SELECT` (case-insensitive).

### 2. Pipeline Reconfiguration (Multi-Service Architecture)
The pipeline consists of multiple services that are automatically started for you, but their configuration files are broken. The intended architecture is:
- **Nginx (Port 8080):** Acts as an API Gateway.
- **Flask API (Port 5000):** Receives ingestion requests and pushes tasks to Redis.
- **Redis (Port 6379):** Message broker.
- **Python Worker (Background):** Reads from Redis, writes relational data to PostgreSQL (Port 5432) and unstructured metadata to MongoDB (Port 27017).

You must fix the configurations so the end-to-end flow works:
* Edit `/home/user/data_pipeline/nginx.conf` so that any request to `/api/` is reverse-proxied to the Flask API at `127.0.0.1:5000`. (Ensure the Nginx service is reloaded/restarted using standard local configuration).
* Edit `/home/user/data_pipeline/.env` so that the Flask API and Worker connect to the correct local ports for Redis (`REDIS_PORT`), PostgreSQL (`PG_PORT`), and MongoDB (`MONGO_PORT`). They are currently set to incorrect dummy values.

Once you have fixed the configurations and restarted the necessary services, verify your setup by running the provided `python3 /home/user/data_pipeline/test_e2e.py` script, which will submit a test CSV through Nginx and verify the databases. Ensure your sanitizer script is ready for automated evaluation.