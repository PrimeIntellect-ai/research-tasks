You are a data scientist working on an ETL pipeline that processes video frame metadata. Due to an orchestration bug, the pipeline retried multiple times, producing duplicate records.

We have a sample video artefact located at `/app/etl_stream.mp4`.

Your task has two parts:

**Part 1: Build a Data Cleaner in Go**
Write a Go program at `/home/user/etl_cleaner.go` and compile it to `/home/user/etl_cleaner`.
This program must read an arbitrary number of CSV lines from `stdin` in the format:
`timestamp,size,type,retry_id`
(e.g., `1.24,4096,I,2`)

Your program must apply the following pipeline transformations:
1. **Timestamp alignment:** Parse `timestamp` as a float64 and round it to the nearest 0.5 (e.g., 1.24 -> 1.0, 1.25 -> 1.5, 1.74 -> 1.5).
2. **Token normalization:** Convert the `type` string to lowercase.
3. **Deduplication (ETL retry resolution):** If multiple records have the same aligned timestamp and normalized type, keep ONLY the record with the highest `retry_id` (integer). If `retry_id`s are tied, keep the one with the highest `size` (integer). If still tied, keep the first one encountered.
4. **Output:** Write the cleaned records to `stdout` in the format: `aligned_time|type|size|retry_id`.
   - `aligned_time` must be formatted to exactly 1 decimal place (e.g., `1.0`, `1.5`).
   - The final output must be sorted by `aligned_time` ascending. If times are equal, sort by `type` alphabetically ascending.

**Part 2: Extract and Process Video Metadata**
Use `ffprobe` to extract the `pkt_pts_time`, `pkt_size`, and `pict_type` for all frames in the first video stream of `/app/etl_stream.mp4`. 
Append a `retry_id` of `1` to every extracted frame. 
Process this generated CSV data through your `/home/user/etl_cleaner` binary and save the output to `/home/user/cleaned_video_data.txt`.