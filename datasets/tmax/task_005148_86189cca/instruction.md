You are acting as a localization engineer for a global analytics firm. We have a broken data pipeline that processes a continuous stream of localized system metrics in JSON-lines format. Our previous parser breaks on specific Unicode escape sequences and fails to properly compute rolling mathematical aggregations across different regional number formats.

Your objective is to write an executable script located at `/home/user/normalize_stream.sh` that takes a stream of JSON-lines from standard input (`stdin`) and outputs processed, normalized data to standard output (`stdout`).

First, examine the image located at `/app/localization_rules.png`. This image contains crucial, mathematically precise configuration parameters for our ETL process that you must recover (using OCR or vision tools). It specifies:
1. The exact window size for our rolling aggregations.
2. The allowed variance threshold for constraint-based data validation.
3. The specific multiplier applied to localized currencies or metrics.

The input JSON-lines format will look like this:
`{"timestamp": 1679900000, "locale": "fr_FR", "raw_value": "1\u00A0234,56", "metric": "latency"}`
Notice the Unicode escape sequences (e.g., non-breaking spaces) and locale-specific decimal separators (commas vs. periods). 

Your script must:
1. Parse the JSON-lines from standard input, properly handling and decoding any Unicode escape sequences.
2. Convert the localized `raw_value` into a standard floating-point number.
3. Apply the mathematical rules found in the `/app/localization_rules.png` image. Specifically, keep a rolling average of the normalized values grouped by the `metric` key using the specified window size.
4. Validate the current value against the constraint: if the current value deviates from the rolling average by more than the allowed variance threshold, cap the value at the threshold limit.
5. Apply the multiplier.
6. Output a standard CSV line to `stdout` for every input line in the format:
   `timestamp,metric,normalized_value,rolling_average,flagged_as_outlier_boolean`

We will evaluate your script by running it against a heavily fuzzed stream of thousands of input lines and comparing its output *bit-for-bit* against our reference implementation. Ensure your script at `/home/user/normalize_stream.sh` is perfectly deterministic, handles edge cases (like the first few values before the window is full), and is marked as executable. You may write the core logic in any language you prefer, provided `/home/user/normalize_stream.sh` wraps it correctly.