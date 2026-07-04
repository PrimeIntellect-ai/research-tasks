You are a localization engineer managing an ETL pipeline that ingests translation activity logs. Recently, an upstream system bug has caused the pipeline to retry failed batches, resulting in duplicate records in the incoming stream.

A legacy, proprietary C++ tool (`/app/oracle`) currently handles streaming ingestion, duplicate removal, time-based bucketing, and metric aggregation. However, we are migrating our stack and need an open-source replacement. Your task is to write a script that exactly replicates the behavior of this oracle.

The log data is provided via standard input (`stdin`) as a continuous stream of CSV lines with the format:
`timestamp,locale,event_type,word_count`
(e.g., `1680000100,es-ES,translated,42`)

Your script must implement the following mathematical and ETL logic to match the oracle:
1. **Streaming & Extraction:** Read from `stdin` line by line.
2. **Deduplication:** The upstream retry bug only causes consecutive identical log entries. If a line is an EXACT string match of the immediately preceding processed line, discard it.
3. **Time-Bucketing:** Convert the Unix `timestamp` to the start of its hour (i.e., bucket it to the nearest multiple of 3600 seconds).
4. **Feature Scoring:** Calculate the activity score based on the event:
   - `translated`: score = `word_count * 1`
   - `reviewed`: score = `word_count * 2`
   - Any other event type (e.g., `failed`, `queued`) has a score of `0` and should NOT be added to the total (they can be dropped from the bucket).
5. **Aggregation:** Sum the scores per time bucket and locale.
6. **Output:** Once `EOF` is reached, output the aggregated data to `stdout` in CSV format: `bucket,locale,total_score`. The output must be sorted chronologically by `bucket` (ascending), and then alphabetically by `locale`. Do not print headers.

You can run `/app/oracle` locally to test your assumptions.
Write your final solution to `/home/user/aggregator.py`. It must accept input via `stdin` and print exactly matching output to `stdout`. Our automated systems will fuzz-test your script against the oracle across thousands of randomized data streams.