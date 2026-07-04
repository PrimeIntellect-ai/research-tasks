We have a local data cleaning pipeline consisting of an Nginx reverse proxy and a backend Rust data processing microservice. The Rust service receives CSV payloads via HTTP POST, cleans them, computes similarity metrics, and returns a formatted report. 

Recently, our data scientists noticed that the Rust service is incorrectly parsing the CSV data: it silently drops or corrupts rows that contain embedded newlines inside quoted strings. 

Your task is to fix and reconfigure the pipeline. The setup is located at `/app/`.

Here are the details:
1. **The Infrastructure**: 
   - An Nginx instance is configured to listen on `127.0.0.1:8000` and proxy requests to the Rust backend.
   - The Rust backend is located in `/app/rust_cleaner`. It currently listens on `127.0.0.1:8080`.
   - The startup script `/app/start.sh` launches both.

2. **The Bug**:
   - The current Rust service in `/app/rust_cleaner/src/main.rs` reads the incoming payload line-by-line using naive string splitting, breaking when `text_a` or `text_b` contains a newline like `"Hello\nWorld"`.
   - You must update the Rust code to properly parse standard CSVs (including embedded newlines). You may use the `csv` crate (which is already in `Cargo.toml`).

3. **The Logic**:
   The CSV will have a header row: `id,text_a,text_b`.
   For each valid row, your Rust service must:
   - Extract `id`, `text_a`, and `text_b`.
   - Compute the Levenshtein distance between `text_a` and `text_b`.
   - Generate a response payload using the exact template format: `[ID: {id}] Distance: {distance}\n` for each row, concatenated together. (Do not include the header in the output).

4. **Security & Protocol**:
   - The Nginx reverse proxy expects requests to `/process`.
   - Your Rust service must ensure it checks for an `Authorization: Bearer data-science-token` header. If missing or invalid, return HTTP 401. 

Fix the Rust code, compile it, and ensure the entire multi-service stack is running so that requests sent to `http://127.0.0.1:8000/process` correctly route to your service, parse the CSV safely, and return the templated similarity report.