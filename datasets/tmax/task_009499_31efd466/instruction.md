You are a localization engineer managing a translation pipeline. An upstream ETL job recently failed and retried automatically, dumping duplicate translation events into our incoming data stream.

We have a raw log file at `/home/user/raw_translations.jsonl`.
Each line is a JSON object with the following fields:
- `tx_id` (integer): The unique transaction ID of the translation.
- `lang` (string): The language code (e.g., "es", "ja", "fr").
- `charset` (string): The character encoding of the payload (e.g., "utf-8", "windows-1252", "shift_jis").
- `payload_b64` (string): Base64-encoded bytes of the translated text.

Your task is to write a Rust application in `/home/user/loc_etl` that processes this data and computes a rolling metric.

Requirements:
1. **Large-file streaming:** Read the JSONL file line-by-line to avoid loading the entire file into memory.
2. **Character encoding handling:** Decode the `payload_b64` into raw bytes, then decode those bytes into a standard Rust UTF-8 `String` using the specified `charset`.
3. **ETL Deduplication:** The retry bug means some `tx_id`s appear multiple times. You must ignore any record if its `tx_id` has already been seen in the stream.
4. **Windowed aggregation:** For each valid, unique record processed, calculate the rolling average of the string's length (in UTF-8 characters, not bytes) for that specific `lang` over the **last 3 unique records** (including the current one).
5. **Output:** Write the results sequentially as they are processed to `/home/user/processed_metrics.csv`.
   - The CSV must have the header: `tx_id,lang,avg_char_count`
   - `avg_char_count` must be formatted to exactly 1 decimal place (e.g., `15.0`, `8.3`).

Example logic for a single language window:
- Record 1 (len 10): avg = 10.0
- Record 2 (len 20): avg = 15.0
- Record 3 (len 15): avg = 15.0
- Record 4 (len 25): avg = 20.0 (average of 20, 15, 25)

Initialize your Rust project, write the code, and run it to produce the final `processed_metrics.csv`. You may use third-party crates like `serde`, `base64`, and `encoding_rs`.