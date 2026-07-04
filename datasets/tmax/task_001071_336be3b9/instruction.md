You are a localization engineer trying to clean up translation rendering telemetry. We have an ETL job that regularly ingests translation render latencies. However, the job produces duplicate records upon retry, and network issues sometimes cause missing data points.

Your task is to write a data processing CLI program that reads a stream of telemetry data, cleans it, and outputs summary statistics.

1. First, there is an image at `/app/locales.png` that contains a list of valid target locales for our current translation sprint. You will need to extract these locale codes.

2. Write a program and save it to `/home/user/process.py`. The program must read JSON-lines (JSONL) from standard input (`stdin`).
Each line may or may not be a valid JSON object. Valid records have the following fields:
- `ts`: An integer representing the timestamp in epoch seconds.
- `loc`: A string representing the locale.
- `lat`: A float representing the translation latency in milliseconds.

3. Your program should process the data with the following logic:
- Ignore any line that is not valid JSON, or is missing any of the three required fields, or where `loc` is not one of the valid locales extracted from the image.
- Group the valid records by `loc`.
- For each locale, sort the records by `ts` ascending.
- Deduplication: Due to ETL retries, there may be multiple records with the exact same `ts` for a given locale. Combine them into a single point by taking the arithmetic mean of their `lat` values.
- Imputation: The telemetry should be reported exactly every 60 seconds. If there is a gap between two adjacent timestamps `ts_a` and `ts_b` in the sorted deduplicated records, you must impute the missing points for every `ts = ts_a + k * 60` (for `k = 1, 2, ...` strictly less than `(ts_b - ts_a) / 60`). The imputed `lat` should be calculated using linear interpolation: `lat = lat_a + (lat_b - lat_a) * (ts - ts_a) / (ts_b - ts_a)`.
- If a locale has fewer than 2 original valid points (with distinct timestamps), discard it.
- Aggregation: For each locale, calculate the overall average latency across all points (both original deduplicated points and imputed points).
- To avoid floating-point discrepancies, calculate the final average latency as a float, multiply by 100, apply the `floor` mathematical function (round down to the nearest integer), and then divide by 100.0.

4. Output Format:
The program must print a single valid JSON object to standard output (`stdout`). The keys should be the locale strings, and the values should be dictionaries containing:
- `start_ts`: The minimum timestamp (int)
- `end_ts`: The maximum timestamp (int)
- `original_points`: The number of unique deduplicated original points (int)
- `imputed_points`: The total number of points added via interpolation (int)
- `avg_lat`: The final aggregated average latency (float, floored as specified above)

Example Output:
```json
{
  "en-US": {
    "start_ts": 100000,
    "end_ts": 100300,
    "original_points": 4,
    "imputed_points": 2,
    "avg_lat": 150.25
  }
}
```
If there are no valid locales with sufficient data, output `{}`.

Make sure your script is executable via `python3 /home/user/process.py`.