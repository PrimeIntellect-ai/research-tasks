You are acting as a Localization Engineer. While updating translations for a major release, you've noticed that the Translation Memory (TM) API service has been experiencing intermittent slowdowns. You have extracted a 24-hour log of translation metrics, but it is in an inconvenient wide format. 

Your task is to write a C++ program that processes this data, reshapes it, aggregates it into time buckets, computes statistical metrics, and identifies anomalies.

Input Data:
The file is located at `/home/user/tm_metrics_wide.csv`.
The CSV has a header and the following columns:
`timestamp_sec, query_id, src_chars, lat_es, chars_es, lat_fr, chars_fr, lat_de, chars_de`
Where `lat_*` is the latency in milliseconds for a language, and `chars_*` is the length of the translated string. Missing or failed queries have `-1` for latency and `-1` for chars. Ignore any language-specific entries for a query where the latency is `-1`.

Write a C++ program at `/home/user/process_metrics.cpp` that performs the following steps:
1. **Wide-to-Long Reshaping:** Convert the data so each record represents a single language's translation (e.g., timestamp, language_code, src_chars, target_chars, latency). The language codes are `es`, `fr`, and `de`.
2. **Time-Based Bucketing:** Group the valid records into 1-hour (3600 seconds) buckets using the `timestamp_sec`. A bucket is identified by its start time: `bucket_ts = (timestamp_sec / 3600) * 3600`.
3. **Summary Statistics & Aggregation:** For each language and each 1-hour bucket, calculate:
   - `avg_latency`: The arithmetic mean of the latency.
   - `avg_expansion_ratio`: The mean of the expansion ratios. (Expansion ratio for a single query = `target_chars / (double)src_chars`).
4. **Normalization:** For each language, across all of its hourly buckets, compute the mean and *population* standard deviation of the `avg_latency`. Then, calculate the Z-score of the `avg_latency` for each bucket (`z_score = (avg_latency - mean) / std_dev`).
5. **Anomaly Detection:** An anomaly is defined as any hourly bucket for a specific language where the latency Z-score is strictly greater than `2.0`.

Your C++ program must output two CSV files:
1. `/home/user/summary.csv`
   Header: `bucket_ts,language,avg_latency,avg_expansion_ratio,latency_zscore`
   Sort the rows alphabetically by `language`, then by `bucket_ts` in ascending order.
   Output all floating-point numbers to exactly 4 decimal places (e.g., using `std::fixed` and `std::setprecision(4)`).

2. `/home/user/anomalies.csv`
   Header: `bucket_ts,language,latency_zscore`
   Contains only the buckets where `latency_zscore > 2.0`.
   Sort the rows alphabetically by `language`, then by `bucket_ts` in ascending order.
   Output Z-scores to exactly 4 decimal places.

Compile your program using `g++ -std=c++17 -O3 /home/user/process_metrics.cpp -o /home/user/process_metrics` and run it to produce the output files.