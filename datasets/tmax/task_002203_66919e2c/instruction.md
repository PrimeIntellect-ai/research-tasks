You are an expert data scientist tasked with cleaning and processing large streams of IoT sensor time-series data. The data is provided in JSON-Lines (JSONL) format, but our current environment has a few issues you need to resolve.

First, our security policies require us to use a vendored version of the `jsonlines` parsing library, which is located at `/app/vendored/jsonlines-3.1.0`. However, a junior developer recently modified it to be "safer", and now it crashes whenever it encounters valid unicode escape sequences in the JSON strings (such as `\u00b0`, which we use for degrees Celsius). You must find and fix the bug in the vendored library so that it correctly parses standard unicode escapes without crashing.

Second, you need to write a data processing script located at `/home/user/process_series.py`. The script must take exactly two command-line arguments: an input JSONL file path and an output JSONL file path.
Execution format: `python /home/user/process_series.py <input_file.jsonl> <output_file.jsonl>` (If you choose to write it in another language, use a wrapper shell script with this exact name and signature).

Your script must implement the following pipeline on the streaming data:
1. **Streaming:** Read the input file line-by-line using the fixed vendored `jsonlines` library. Do not load the entire file into memory.
2. **Deduplication:** The JSON records have a `timestamp` (integer) and a `sensor_payload` (a dictionary). If a record has the exact same `sensor_payload` as the *immediately preceding* valid record, it is considered a duplicate and must be dropped.
3. **Imputation:** The `timestamp` field represents seconds. If there is a gap between consecutive records (e.g., timestamps 10 then 13), you must insert the missing records (11 and 12). The `sensor_payload` for these inserted records should be a copy of the previous record, but its nested `value` field (a float) must be linearly interpolated between the start and end of the gap.
4. **Sanitization:** Some sensor nodes have been compromised and are leaking PII into the nested `sensor_payload`. You must drop any record (and do not use it for imputation) if the key `"ssn"` or `"email"` appears anywhere at any depth within the parsed JSON record.

Sample data for your own testing is available in `/home/user/sample_data/`. 
Ensure your script writes the final processed JSONL to the specified output file path.