You are tasked with fixing a configuration management pipeline that is suffering from duplicated ETL records due to retries, and recovering some missing metadata from a recorded video of a server deployment.

Part 1: Video Analysis
We lost the deployment logs for a recent update, but we have a screen recording of the deployment dashboard. In the video, whenever a deployment failed and triggered a retry, the dashboard flashed a solid blue screen. 
You need to analyze the video located at `/app/deploy_recording.mp4`. Count the exact number of frames where the screen is completely blue (defined as average pixel values of Red < 50, Green < 50, and Blue > 200). 
Write this integer count to `/home/user/blue_frames.txt`.

Part 2: Configuration Deduplication
Write a Python script at `/home/user/dedup.py` that reads a stream of JSON records from standard input (one record per line) and outputs deduplicated records to standard output, while writing logs to standard error.

Input Format:
Each line is a JSON object with the following keys:
- `timestamp`: string
- `host`: string
- `config`: string of key-value pairs separated by commas (e.g., "Mem=4G,Cpu=2,disk=100G")
- `is_retry`: boolean

Processing Rules:
1. Line Parsing: If a line cannot be parsed as valid JSON, print `ERROR: Invalid JSON` to standard error and skip the line.
2. Normalization: For the `config` string, split the pairs by comma. Convert all keys (the part before the `=`) to lowercase. Sort the key-value pairs alphabetically by key. Rejoin them into a single string separated by commas. (e.g., "Mem=4G,Cpu=2,disk=100G" becomes "cpu=2,disk=100G,mem=4G").
3. Hashing: Compute the SHA-256 hex digest of the string formed by concatenating the `host` and the normalized `config` string (i.e., `host + normalized_config`).
4. Deduplication: Keep track of seen hashes. If a hash has not been seen before, it is a new record. If it has been seen, it is a duplicate.
5. Output: 
   - For a new record, print it as a single-line JSON string to standard output. The output JSON must include the original `timestamp`, `host`, `is_retry`, the newly normalized `config`, and a new key `config_hash` containing the computed SHA-256 hash. Do not output spaces after colons/commas if possible, or just use `json.dumps(obj, separators=(',', ':'))`. Sort the keys in the output JSON alphabetically.
   - For a duplicate record, do NOT output it to standard output. Instead, print `DUPLICATE: <hash>` to standard error.
6. Logging/Monitoring Summary: After processing all input lines (EOF reached), print exactly this template string to standard error: `SUMMARY: Processed <N> valid records, <D> duplicates found.` where `<N>` is the total number of valid JSON lines read, and `<D>` is the number of duplicates dropped.

Example standard error outputs:
```
ERROR: Invalid JSON
DUPLICATE: 3a7b...
SUMMARY: Processed 5 valid records, 1 duplicates found.
```

Your script must be deterministic and exactly match our reference implementation's behavior. We will fuzz test your `dedup.py` script with thousands of random JSON records to verify exact compliance.