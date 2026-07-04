You are a data engineer tasked with building a resilient, high-throughput ETL pipeline component.

We have a custom, high-performance CSV parsing library vendored at `/app/vendored/fastcsv-1.0.4`. It was recently modified by a junior engineer to support parallel parsing, but they accidentally broke the build configuration. Because of this, it currently falls back to a slow, pure-Python implementation that silently drops CSV rows containing embedded newlines. 
Your first goal is to debug and fix the build configuration for this vendored package so the C-extension compiles correctly, and then install it into your local environment.

After fixing the library, you must write a data transformation script at `/home/user/stream_etl.py` that utilizes this library.

The script must:
1. Read a continuous stream of raw binary CSV data from `stdin` (large-file streaming).
2. Process the data in parallel (you may use Python's `multiprocessing` or similar, as the stream can be highly voluminous).
3. Handle mixed character encodings. The CSV has three columns: `id` (integer), `encoding` (string, e.g., 'utf-8', 'iso-8859-1', 'windows-1252'), and `payload` (string, potentially containing embedded newlines and commas).
4. For each row, decode the `payload` bytes using the specified `encoding`. If a decoding error occurs, replace invalid characters with the standard Unicode replacement character (U+FFFD).
5. Output a stream of JSON lines (JSONL) to `stdout`. Each JSON object must have three keys:
   - `"id"`: The integer ID.
   - `"payload_length"`: The character count of the decoded payload.
   - `"normalized_payload"`: The correctly decoded payload string (UTF-8).

Your script must perfectly replicate the output of our reference pipeline, which handles edge cases (like escaping, embedded newlines, and massive continuous streams) perfectly. Our automated test suite will aggressively fuzz your script with randomly generated CSV streams to ensure it is bit-exact equivalent to the reference implementation.

Please write the `/home/user/stream_etl.py` script. The script should be executable (e.g., `chmod +x`).