I need you to fix and reconfigure our data cleaning and analysis pipeline. Our previous data scientist left behind a multi-service architecture under `/home/user/app/` that is currently broken.

The system consists of three services:
1. `data_ingest` (Mock Python HTTP server at `/home/user/app/ingest/`): Serves raw, noisy text data on port 8000.
2. `cleaning_worker` (Rust application at `/home/user/app/cleaner/`): Meant to fetch data from `data_ingest`, clean it (tokenize, remove punctuation, lowercase), and expose the processed dataset on port 8080.
3. `model_serving` (Rust application at `/home/user/app/serving/`): Meant to fetch cleaned numerical data from `cleaning_worker`, run a basic linear combination (classification scoring), and serve predictions on port 9000.

Your tasks:
1. Complete the Rust implementation in `/home/user/app/cleaner/src/main.rs`. The code currently fails to compile because the tokenization and dataset preparation logic is missing. You must implement the `clean_and_tokenize` function to:
   - Convert all text to lowercase.
   - Remove all characters except alphanumerics and whitespace.
   - Split by whitespace into tokens.
   - Return a JSON array of these tokens.
2. Configure the services to communicate. The `model_serving` service uses an environment file `/home/user/app/serving/.env`. You need to set `CLEANER_URL=http://localhost:8080/data` in this file.
3. Start all three services in the background. Note: The Python service can be started with `python3 -m http.server 8000` in its directory (which contains a `data.json` file). The Rust services must be built using `cargo build --release` and then executed.
4. Ensure the end-to-end pipeline works. When a client sends an HTTP GET request to `http://localhost:9000/predict`, the `model_serving` service should successfully orchestrate the pipeline and return the evaluated numerical score as a JSON object: `{"status": "success", "score": <float>}`.

Create a log file at `/home/user/pipeline_status.log` containing the word "READY" once all services are bound to their respective ports and the `/predict` endpoint is operational.