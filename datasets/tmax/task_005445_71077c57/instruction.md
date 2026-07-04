You are a data engineer responsible for a text-processing ETL pipeline. Recently, our pipeline has been failing silently—similar to a misconfigured plotting script that outputs blank images without throwing errors. The current Python-based tokenizer is dropping complex Unicode text and failing to generate valid token IDs for our machine learning dataset. 

Additionally, our multi-service setup (Nginx -> Flask -> Redis) is currently broken due to configuration mismatches after a recent migration.

Your task is twofold:

**Part 1: Fix the Service Configuration**
In `/home/user/pipeline/`, you will find a multi-service setup consisting of an Nginx reverse proxy, a Flask API (`api.py`), and a Redis backend.
1. The Nginx configuration (`/home/user/pipeline/nginx.conf`) is supposed to listen on port 8080 and route requests to the Flask API. However, it is pointing to the wrong upstream port. Fix it to point to the correct Flask port (5000).
2. The Flask API (`api.py`) pushes jobs to Redis. Fix the Redis connection string in `api.py` so it connects to the default Redis port (6379) instead of the erroneous port currently hardcoded.
3. Ensure Nginx, Redis, and the Flask app are running so that a POST request to `http://127.0.0.1:8080/tokenize` with a JSON payload `{"text": "..."}` successfully enqueues data to Redis. (You can run `redis-server --daemonize yes` and start the others in the background).

**Part 2: Build a Robust Rust Tokenizer**
The Flask API delegates tokenization to a binary expected at `/home/user/bin/tokenizer`. You must write this binary in Rust to replace the faulty Python logic.

Create a Rust project in `/home/user/rust_tokenizer` and compile a release binary. Copy the compiled binary to `/home/user/bin/tokenizer` (create the directory if it doesn't exist).

The binary must read raw text from `stdin` (until EOF) and write a single JSON array of unsigned 32-bit integers to `stdout`.

**Tokenization & Hashing Rules:**
1. **HTML Stripping:** Remove all HTML/XML tags. A tag is defined as anything starting with `<` and ending with `>` (inclusive, non-greedy).
2. **Lowercasing:** Convert all remaining text to lowercase.
3. **Punctuation Removal:** Retain ONLY alphanumeric characters (A-Z, a-z, 0-9) and spaces. Completely remove all other symbols, punctuation, and control characters.
4. **Tokenization:** Split the resulting string by whitespace into a list of individual tokens.
5. **Numerical Hashing (Token IDs):** Convert each token into a 32-bit ID using the **FNV-1a 32-bit** hash algorithm. 
   - FNV offset basis: `2166136261` (0x811c9dc5)
   - FNV prime: `16777619` (0x01000193)
   - Iterate over the UTF-8 bytes of the token.
6. **Output:** Print the resulting token IDs as a JSON array (e.g., `[234234, 897897]`) to `stdout`. Do not print anything else.

Ensure your Rust implementation handles edge cases like empty inputs, strings with only HTML tags, and heavy Unicode correctly. The automated verifier will strictly test your binary against a reference oracle using thousands of randomly generated edge-case strings.