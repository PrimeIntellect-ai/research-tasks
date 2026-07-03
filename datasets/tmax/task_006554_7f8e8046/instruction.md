You are an integration developer testing a set of math-heavy API endpoints for a distributed system. The system's API Gateway dumps mock latency payloads from different backend versions into a specific directory. Your task is to analyze these fixtures, filter them based on semantic versioning rules, merge the latency data, sort it, and compute the difference against a baseline.

Here is your objective:

1. **Setup Test Fixtures:**
   First, create a directory `/home/user/api_mocks` and populate it with the following JSON test fixtures representing mock API payloads:
   - `payload_a.json`: `{"api_version": "1.2.5", "data": [45, 60, 32]}`
   - `payload_b.json`: `{"api_version": "1.4.1", "data": [55, 42, 88]}`
   - `payload_c.json`: `{"api_version": "1.5.0", "data": [12, 18]}`
   - `payload_d.json`: `{"api_version": "2.0.1", "data": [99, 100, 101]}`
   - `payload_e.json`: `{"api_version": "1.9.9", "data": [77, 81]}`

   Also, create a baseline file at `/home/user/baseline_latencies.txt` containing the following numbers, one per line:
   ```
   12
   15
   18
   42
   55
   77
   88
   ```

2. **Develop the Rust Analyzer:**
   Create a new Rust binary project at `/home/user/latency_analyzer`. 
   Write a Rust program that:
   - Reads all JSON files from `/home/user/api_mocks`.
   - Parses the `api_version` field using Semantic Versioning rules.
   - Filters and **keeps only** the payloads where the `api_version` is compatible with `^1.4.0` (meaning `>= 1.4.0` and `< 2.0.0`).
   - Extracts the integers from the `data` array of the matching payloads.
   - Merges all valid integers into a single collection.
   - Sorts the collection in ascending mathematical order.
   - Writes the sorted integers (one per line) to `/home/user/merged_latencies.txt`.

   *Hint: You will likely need the `serde`, `serde_json`, and `semver` crates.*

3. **Diff the Results:**
   Once your Rust program has successfully generated `/home/user/merged_latencies.txt`, use the standard bash `diff` command to diff your generated file against `/home/user/baseline_latencies.txt`. 
   
   Run `diff -u /home/user/baseline_latencies.txt /home/user/merged_latencies.txt > /home/user/latency_diff.patch`. (It is expected that they might differ; we just need the diff patch created successfully).

Ensure all resulting files are exactly where specified. Do not include any extra text in the `merged_latencies.txt` file other than the integers.