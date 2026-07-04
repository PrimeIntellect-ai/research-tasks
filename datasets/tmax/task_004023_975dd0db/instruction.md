You are a localization engineer analyzing translator throughput to optimize our localization pipelines. You've been provided with a large JSON Lines log file containing millions of translation events, located at `/home/user/translation_events.jsonl`.

Each line in the log represents a translation commit and has the following format:
`{"ts": <unix_timestamp>, "lang": "<locale_code>", "words": <integer>}`

We need a high-performance C++ tool to compute windowed aggregations of this data. A skeleton script `/home/user/aggregate_throughput.cpp` is provided, but it relies on `simdjson` for fast parsing. We have vendored the `simdjson` source code in `/app/simdjson`. 

Your tasks:
1. The vendored `simdjson` package in `/app/simdjson` has a configuration error preventing it from building correctly. Identify and fix the perturbation in its build files so you can compile and install it or link against it.
2. Complete the C++ program `/home/user/aggregate_throughput.cpp` to parse the JSONL file.
3. For each `lang`, aggregate the `words` into 1-hour tumbling buckets (using the `ts` field, where buckets start at Unix epoch hour boundaries, i.e., `ts - (ts % 3600)`).
4. Compute summary statistics: For each bucket, calculate the total `words` in that hour, and the *3-hour rolling average* of words (the mean of the total words in the current 1-hour bucket and the immediately preceding two 1-hour buckets). If a preceding bucket has no events, treat its word count as 0.
5. Compile your C++ program and run it against `/home/user/translation_events.jsonl`.
6. Output the results to `/home/user/throughput_stats.csv` with the exact header: `bucket_ts,lang,hourly_words,rolling_3h_avg`
Sort the output chronologically by `bucket_ts` (ascending), then alphabetically by `lang`. `rolling_3h_avg` should be formatted to 2 decimal places.

Ensure your C++ program is highly efficient. Your final executable should be placed at `/home/user/aggregator`.