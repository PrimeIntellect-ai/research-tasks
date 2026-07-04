We are building a configuration tracking manager that ingests configuration snapshots from multiple servers, filters out malicious or unauthorized configurations, and produces a normalized, gap-filled timeline of changes.

You need to implement two separate Python tools to accomplish this workflow.

**Part 1: Adversarial Configuration Detector (`/home/user/detector.py`)**
We receive configuration snapshots in JSON format. Unfortunately, some snapshots have been tampered with by an attacker attempting privilege escalation or arbitrary execution. 
You must write a classifier script at `/home/user/detector.py`. 
It will be invoked as: `python3 /home/user/detector.py <path_to_config.json>`
* It must exit with code `0` if the configuration is safe ("clean").
* It must exit with code `1` if the configuration is malicious ("evil").

A configuration is considered "evil" if any string value anywhere in the JSON (nested at any depth, in any key or array) contains:
1. The exact substring `LD_PRELOAD`
2. Any file path starting exactly with `/tmp/` or `/var/tmp/`
Otherwise, it is "clean".

**Part 2: Configuration ETL Pipeline (`/home/user/etl.py`)**
There is an image artefact located at `/app/system_params.png`. It contains a snapshot of a dashboard with two critical parameters you must extract (using an OCR tool like `tesseract`):
* `SALT`: A secret string used for deduplication.
* `INTERVAL`: A time frequency (e.g., `15T` or `30T` representing minutes).

You must write a script at `/home/user/etl.py` that takes a directory of clean JSON configuration files, processes them, and outputs a CSV file at `/home/user/timeline.csv`.
* Run command: `python3 /home/user/etl.py <input_dir> /home/user/timeline.csv`
* **Input Files:** JSON files containing `{"server_id": "...", "timestamp": "YYYY-MM-DDTHH:MM:SSZ", "payload": {...}}`.
* **Sorting & Grouping:** Group records by `server_id` and sort them chronologically by `timestamp`.
* **Hash-based Deduplication:** For each server, compute a SHA-256 hash of the `payload` stringified as compact JSON (no spaces, keys sorted alphabetically) concatenated with the extracted `SALT` (e.g., `SHA256(json_string + SALT)`). If a configuration's hash is identical to the *immediate preceding* configuration for that same server, it is a duplicate and should be dropped.
* **Bucketing & Gap-filling:** Generate a continuous time series of buckets of size `INTERVAL` (extracted from the image), starting from `2024-01-01T00:00:00Z` to `2024-01-01T23:59:59Z`. For every bucket and every `server_id` present in the dataset, output the hash of the active configuration. If a server has no new configuration in a given bucket, carry forward the hash from the previous bucket (gap-filling). If no configuration has been seen yet for that server, output `EMPTY`.
* **Output Format:** The output CSV must have a header: `bucket_start,server_id,config_hash`. Rows should be sorted by `bucket_start` ascending, then `server_id` ascending. `bucket_start` must be in `YYYY-MM-DDTHH:MM:SSZ` format.

Ensure your code is robust, fully contained, and executable in a standard Linux environment.