You are a Machine Learning Engineer preparing a training dataset pipeline. We have a microservice architecture for preprocessing raw text data into embeddings. 

Currently, our pipeline has two background services:
1. **Redis Cache** (running on `127.0.0.1:6379`)
2. **Embedding API** (a mock FastAPI service running on `http://127.0.0.1:8000`)

Your task is to implement the main data processing worker in **Rust**. You must create a Rust project at `/home/user/rust_worker` and build a release binary that will be located at `/home/user/rust_worker/target/release/process_data`.

### Application Specifications

The Rust worker must operate as a command-line Unix filter (reading from `stdin` line by line, and writing to `stdout` line by line).

**Input Format:**
Standard input will consist of JSON Lines. Each line is a JSON object:
`{"id": "doc_123", "text": "Some raw, un-normalized text!! 123"}`

**Processing Steps for each line:**
1. **Tokenization & Normalization:**
   - Extract the `text` field.
   - Convert the entire string to lowercase.
   - Replace any character that is NOT an ASCII alphanumeric character (`a-z`, `0-9`) with a single space.
   - Split the resulting string by whitespace into an array of strings (tokens), ignoring empty tokens.
   - Truncate this array to a maximum of 10 tokens.
   - Re-join these tokens with a single space to form the `normalized_text`.

2. **Similarity Search / Cache Retrieval:**
   - Connect to Redis at `127.0.0.1:6379` (no password).
   - Check if the key `embed:{normalized_text}` exists.
   - If it exists, parse its value as a JSON array of integers, which is the embedding.

3. **Embedding Computation (if cache miss):**
   - If the key does not exist in Redis, make an HTTP `POST` request to `http://127.0.0.1:8000/embed`.
   - The payload must be JSON: `{"text": "the normalized_text string"}`.
   - The API will respond with JSON: `{"embedding": [1, 5, 22, ...]}`.
   - Store the retrieved embedding array as a JSON string in Redis under the key `embed:{normalized_text}`.

4. **Output Generation:**
   - Write exactly one JSON line to `stdout` per input line.
   - Format: `{"id": "doc_123", "tokens": ["some", "raw", "un", "normalized", "text", "123"], "embedding": [1, 5, 22, ...]}`
   - Do not print any extraneous logs or text to `stdout`, as it will break downstream JSON parsers. If you need to log errors or debug info, use `stderr`.

### Setup
A script is provided at `/app/start_services.sh` to start Redis and the Embedding API. You must ensure your Rust worker connects to them correctly. Use `cargo init` to start your project. You can use standard crates like `reqwest`, `serde`, `serde_json`, `redis`, and `tokio`. Ensure you compile your final binary using `cargo build --release`.