You are an ETL data engineer building a pipeline that aligns noisy sensor telemetry with video frame metadata. 

We have a reference video located at `/app/reference_feed.mp4`. 
Your goal is to write a Python CLI program at `/home/user/pipeline.py` that processes raw sensor data, aligns it with the video's keyframe timestamps, and calculates a similarity metric.

Your script must operate exactly as follows to pass the automated verification tests:

**1. Extract Video Reference Data (One-time extraction)**
Using `ffprobe`, extract the `pkt_pts_time` (as a float) and `pkt_size` (as an integer) for all **video stream packets** in `/app/reference_feed.mp4` that are marked as keyframes (`flags=K_`).
Store this reference data in memory or save it locally. This forms your "Master Timeline".

**2. CLI Interface**
Your script will be invoked as:
`python3 /home/user/pipeline.py <path_to_input.csv>`
It must print a single valid JSON string to `stdout` and exit with code 0.

**3. Process the Input CSV**
The input CSV has columns: `timestamp` (float), `sensor_id` (string), `value` (float).
- Pivot the dataset so that `timestamp` is the index, and each unique `sensor_id` is a column. Sort the index.
- Resample the time-series to a regular grid of `0.5` second intervals. Start the grid at `floor(min_timestamp)` and end at `ceil(max_timestamp)` of the CSV.
- Fill gaps using Forward Fill (ffill). If any NaNs remain (e.g., at the beginning), fill them with `0.0`.
- Calculate the "Euclidean distance from origin" for each row. (i.e., `sqrt(sum(v^2))` for all sensor values in that row).

**4. Join & Merge**
- For each keyframe extracted from the video, round its `pkt_pts_time` to the nearest `0.5` (to match the resampled grid).
- Perform a Left Join: for each rounded keyframe timestamp, look up the computed Euclidean distance in your resampled grid. If the timestamp does not exist in the grid (out of bounds), use `-1.0`.
- Compute a "Similarity Score": `abs(distance - pkt_size) / pkt_size`. Round this score to exactly 4 decimal places.

**5. Output format**
Print a JSON list of objects to `stdout`, ordered by the original keyframe `pkt_pts_time` ascending:
`[{"pts": <original_pkt_pts_time_float>, "rounded_pts": <rounded_float>, "similarity": <float>}, ...]`

Ensure your code is perfectly deterministic and matches these rules exactly, as it will be tested against a hidden oracle using hundreds of randomly generated CSVs.