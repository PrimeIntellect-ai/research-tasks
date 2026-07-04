Build an idempotent audio ETL pipeline in Bash that extracts volume metrics, standardizes the data, computes similarity, and serves the results over HTTP. 

You are an automation specialist dealing with a flaky scheduler that often triggers jobs twice, causing duplicate records. Your task is to process an audio recording of a mechanical test and serve the analysis.

1. **Extract and Resample:**
Create a pipeline script at `/home/user/pipeline.sh`. The script must process the audio file located at `/app/test_signal.wav`. 
Using `ffmpeg` or `ffprobe`, extract the mean volume (in dB, or raw RMS) for every 1-second window for the first 10 seconds of the file. 
Resample/gap-fill: You must generate exactly 10 records (representing seconds 0 through 9). If a second has no audio data, fill the value with a standard silence floor of `-90.0` dB.

2. **Normalize and Deduplicate (ETL Idempotency):**
Normalize all dB values to a positive scale where `-90.0` dB is `0.0`, and `0.0` dB is `100.0`. 
Save the records to `/home/user/metrics.csv` in the format `timestamp,normalized_value`. 
Your script must be idempotent: if `/home/user/pipeline.sh` is executed multiple times, `/home/user/metrics.csv` must never contain duplicate timestamps (e.g., if it runs twice, there should still only be 10 lines, overwriting or ignoring duplicates, not appending endlessly).

3. **Aggregation and Similarity DAG:**
Compute the average normalized volume across the 10 seconds. 
Compute the Euclidean distance between your 10-second normalized volume array and this reference array: `[10, 20, 10, 20, 10, 20, 10, 20, 10, 20]`.
Output these findings to `/home/user/summary.json` with the keys: `average_volume`, `euclidean_distance`, and `record_count`.

4. **Serve via HTTP:**
Write a daemon script at `/home/user/server.sh` (using `nc` or `socat` in Bash) that binds to `0.0.0.0:8080`. 
When it receives an HTTP `GET /api/v1/metrics` request, it must respond with a valid `200 OK` HTTP response containing the exact contents of `/home/user/summary.json` as the body, with a `Content-Type: application/json` header.

Ensure both scripts are executable. Start the server in the background before finishing.