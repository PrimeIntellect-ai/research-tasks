You are tasked with fixing and assembling a broken data ingestion pipeline for our data science team. The current setup drops valuable customer reviews because the data processor incorrectly splits CSVs by newline, corrupting rows with embedded newlines in the review text. 

You need to fix the Python worker, configure an Nginx reverse proxy, and ensure the whole multi-service architecture runs smoothly.

Here is the system architecture:
1. **Redis**: Running as a message broker on `127.0.0.1:6379`.
2. **Ingestion Service**: A Flask app located at `/app/ingestion.py` that listens on `127.0.0.1:5001`. It receives raw POST requests and pushes them to a Redis list named `raw_data`.
3. **Data Worker**: A buggy script located at `/app/worker.py`. It pulls from Redis, processes data, and writes to a SQLite database.
4. **Query Service**: A Flask app at `/app/query.py` that listens on `127.0.0.1:5002` and reads from the SQLite database.
5. **Nginx Proxy**: Should listen on `127.0.0.1:8080`.

**Your Tasks:**
1. **Modify `/app/worker.py`**:
   - Make it continuously read JSON-encoded payloads from the Redis list `raw_data`. Each payload has a `format` key (`csv` or `json`) and a `data` key (a string of the raw data).
   - Fix the CSV parsing: The `data` string can contain CSV rows with embedded newlines in the `review_text` column. Do not just use `.split('\n')`. Use proper CSV parsing.
   - For JSON format, parse the string as a JSON array of objects.
   - Both formats will yield records with: `id` (string), `timestamp` (string), and `review_text` (string).
   - **Normalize**: Standardize the `timestamp` field to `YYYY-MM-DD HH:MM:SS` format. Input timestamps might be Unix epochs (e.g., `1672531200`) or dates like `12/31/2022 10:00`.
   - **Feature Extraction**: Add a new integer column called `word_count` which is the number of whitespace-separated words in `review_text`.
   - Write the cleaned records to a SQLite database at `/home/user/pipeline/clean.db` in a table named `reviews` (columns: `id` TEXT PRIMARY KEY, `timestamp` TEXT, `review_text` TEXT, `word_count` INTEGER).

2. **Configure Nginx**:
   - Write an nginx configuration file at `/home/user/nginx.conf`.
   - It must listen on `127.0.0.1:8080`.
   - Route `POST /ingest` to `http://127.0.0.1:5001/ingest`.
   - Route `GET /query` to `http://127.0.0.1:5002/query`.

3. **Service Orchestration**:
   - Start Redis, Nginx (using your config), both Flask apps, and your worker script in the background.

The evaluation will programmatically send CSVs with embedded newlines to the ingestion endpoint on port 8080 and immediately query the processed results to verify normalization and feature extraction.