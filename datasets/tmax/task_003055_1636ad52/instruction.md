You are building a configuration manager that tracks distributed mathematical model parameters across a fleet of microservices. Configurations are streamed as JSON-lines, but the raw stream is polluted with malformed payloads, unicode-spoofing attacks, and duplicate submissions. 

You must complete a two-part task to filter these configurations and route them through a multi-service pipeline.

**Part 1: The Adversarial Sanitizer**
Write a script at `/home/user/sanitizer.py` that takes a single file path as a command-line argument. The script must read the file (which contains one JSON object per line) and print only the valid JSON lines to standard output. 

A line is strictly **INVALID** (and must be dropped) if it meets *any* of the following conditions:
1. It contains invalid JSON or broken Unicode escape sequences (e.g., unpaired surrogates).
2. Any string field contains Unicode Bidirectional Control Characters (such as U+202E Right-to-Left Override).
3. The JSON object contains a `weights` key (a list of floats) where any value is non-finite (`NaN`, `Infinity`, `-Infinity`), or the sum of the weights is not equal to `1.0` (allowing a tolerance of `1e-6`).

**Part 2: The Pipeline Worker**
We have a multi-service setup. Run `/app/start_services.sh` to start the backend services:
*   **Redis** (localhost:6379): Acts as the message broker.
*   **Emitter** (localhost:8001): Simulates the fleet, continuously pushing JSON-lines configurations to the Redis list named `raw_configs`.
*   **Store API** (localhost:8002): The central database API. It accepts `POST` requests at `http://127.0.0.1:8002/api/store` with a JSON payload.

Write a continuous worker script at `/home/user/worker.py` that does the following:
1. Connects to Redis and continuously pops messages from the `raw_configs` list (e.g., using `BLPOP`).
2. Applies the exact same sanitization rules as Part 1. Drops invalid messages.
3. For valid messages, applies **NFKC normalization** to the `service_name` string field.
4. **Deduplicates** configurations on the fly: 
   * Compute a canonical representation of the configuration: sort all dictionary keys, ensure strings are NFKC normalized, and round all floats in the `weights` array to exactly 4 decimal places.
   * Compute the SHA-256 hash of this canonical JSON string.
   * Maintain a record of seen hashes in memory (or Redis). If the hash has been seen before, drop the message.
5. If the message is valid and unique, send it via a `POST` request to the Store API (`http://127.0.0.1:8002/api/store`) with the `Content-Type: application/json` header.

Leave `/home/user/worker.py` running in the background when you consider the task complete. The automated system will inject a test payload into Redis and verify it arrives correctly deduplicated and sanitized at the Store API.