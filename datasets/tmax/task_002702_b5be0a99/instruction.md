As an automation specialist, you are debugging a fragile data pipeline. We have a legacy, stripped proprietary binary located at `/app/price_aggregator` that calculates trading metrics. Unfortunately, it processes CSVs using naive line-breaks. If the data contains embedded newlines inside quoted fields, the binary silently drops rows and corrupts the pipeline.

You need to create a robust Python pre-processing filter at `/home/user/preprocess.py` that reads a CSV from standard input (`stdin`) and writes the corrected CSV to standard output (`stdout`).

The input CSV has the following columns: `timestamp,tx_id,price,comment` (where `timestamp` is an integer UNIX epoch). 

Your script must perform the following operations in order:
1. **Hash-based Deduplication**: Remove any duplicate rows based on the `tx_id` column. If multiple rows have the same `tx_id`, keep only the first one encountered.
2. **Sanitization**: In the `comment` field, replace any embedded newlines (`\n` or `\r\n`) with a single space character.
3. **Resampling & Gap-Filling**: The pipeline requires a continuous 1-second interval time-series. Find the minimum and maximum `timestamp` in the deduplicated data. For any missing integer timestamps between min and max, insert a new row. The `price` should be forward-filled from the most recent valid row. The `tx_id` should be `GAP` and the `comment` should be `FILLED`.
4. **Pipeline Logging**: As you output the rows, compute a rolling moving average of the `price` over a 3-row window (including the current row and up to 2 previous rows). For every row, print `LOG: <timestamp> <rolling_avg>` to `stderr`, formatted to 2 decimal places.

Ensure your output CSV headers match the input perfectly, and that the output strictly uses standard CSV quoting where necessary. You can use `/app/price_aggregator` to test how the legacy system behaves with clean vs malformed data.