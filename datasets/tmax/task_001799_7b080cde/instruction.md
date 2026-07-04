You are a localization engineer tasked with modernizing a translation pipeline. We have a legacy system that serves raw translation files over HTTP, but they are in various legacy character encodings. We need to fetch these, decode them to UTF-8, cache them in a Redis database, and serve them via a new HTTP API written in Rust.

Here is the setup in the `/app/` directory:
- `start_services.sh`: A script that brings up a Redis instance (port 6379) and a legacy Python HTTP server (port 8080) hosting the raw translation files.
- The raw files hosted on port 8080 are:
  - `http://localhost:8080/fr.csv` (Encoded in ISO-8859-1) - format: `KEY,VALUE`
  - `http://localhost:8080/ja.csv` (Encoded in Shift_JIS) - format: `KEY,VALUE`

Your task:
1. Run `/app/start_services.sh` to start the backend services.
2. Create a Rust application in `/home/user/translation_service` (initialize it with `cargo new`).
3. The Rust application must perform an ETL process on startup:
   - Fetch the files from `http://localhost:8080/fr.csv` and `http://localhost:8080/ja.csv`.
   - Decode them from their respective legacy encodings (ISO-8859-1 and Shift_JIS) into UTF-8.
   - Parse the CSV data.
   - Connect to Redis at `redis://127.0.0.1:6379` and store each key-value pair under the Redis key `locale:{lang}:{key}`. For example, the `GREETING` key in the Japanese file should be stored in Redis under the key `locale:ja:GREETING`.
   - Log the successful processing of each file by appending a line to `/home/user/pipeline.log` in the exact format: `[SUCCESS] Processed {lang} - {count} keys loaded.`.
4. After the ETL process completes, the Rust application must start an HTTP server listening on `127.0.0.1:9000`.
5. The HTTP server must have a single endpoint: `GET /translate/{lang}/{key}`. 
   - It should query Redis for `locale:{lang}:{key}`.
   - If found, it must return an HTTP 200 OK with the UTF-8 translated string as plain text.
   - If not found, it must return an HTTP 404 Not Found.

Run your Rust application in the background so it continues to listen on port 9000. 
You can use any standard Rust crates (e.g., `reqwest`, `encoding_rs`, `redis`, `axum`, `tokio`).