I need you to build a robust data processing pipeline for our configuration management system. We track configuration state changes across thousands of servers using JSON-lines logs. However, we're encountering issues with our parser, and we're being targeted by anomalous/malicious configuration payloads. 

Your task involves three main stages:

**Stage 1: Fix the Vendored Parser**
We vendor the `jsonlines` library to handle streaming logs. The source is located at `/app/vendored/jsonlines-3.1.0`. 
Recently, someone modified `jsonlines/jsonlines.py` to "optimize" string reading, but now it breaks when encountering valid Unicode escape sequences (e.g., `\u0041`) inside JSON values, raising a `ValueError`. 
Find the perturbation in `/app/vendored/jsonlines-3.1.0/jsonlines/jsonlines.py` (look near the `Reader` class setup) and fix it so it properly handles unicode escapes. You must install this package locally after fixing it.

**Stage 2: Metric Aggregation Pipeline**
Write a Python script `/home/user/process_metrics.py` that reads a JSON-lines file of configuration changes. Each line has: `{"timestamp": int, "server_id": str, "config_state": dict, "memory_allocated": int}`.
Using the fixed `jsonlines` library, your script must:
1. **Hash-based Deduplication:** Compute the SHA-256 hash of the sorted, serialized `config_state`. For each `server_id`, ignore consecutive lines where the `config_state` hash hasn't changed.
2. **Rolling Statistics Computation:** For the deduplicated events per `server_id`, calculate a rolling 3-event average of `memory_allocated`.
3. **Data Sampling and Stratification:** Output a stratified sample. For each `server_id`, output the single event that has the highest `memory_allocated` among its deduplicated events.
4. **Summary Statistics:** Output a file `/home/user/metrics_summary.csv` containing the `server_id`, `total_deduplicated_events`, and `max_memory_allocated`.

**Stage 3: Adversarial Configuration Filter**
We are receiving malicious payloads. Create a Python script `/home/user/filter_configs.py` that takes an input file path and an output file path as arguments (`python filter_configs.py <input.jsonl> <output.jsonl>`).
This script must inspect each JSON line. It must REJECT (drop) the line if:
- The JSON contains deeply nested dictionaries (depth > 5).
- Any string value in `config_state` contains shell metacharacters (`;&|`).
- It fails to parse using the standard JSON specification.
It must PRESERVE all other lines exactly as they appeared.

Ensure all scripts are executable and rely only on Python standard libraries and the fixed `jsonlines` package.