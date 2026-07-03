You are tasked with building a Go-based data processing pipeline and HTTP API to analyze video frame metadata. A video file has been provided at `/app/data_video.mp4`.

As a data analyst, you need to extract and clean frame metadata, identify anomalies (changepoints), and remove duplicates, making the results available via a local web service.

Step 1: Data Extraction & Streaming
Using `ffprobe`, extract the packet metadata for the video stream in the file `/app/data_video.mp4`. You must extract `pts_time`, `size`, `flags`, and any stream `tags`. Output this data in JSON or CSV format and process it using a Go application. The Go application should stream the data rather than loading it all into memory at once, as the file could theoretically be very large.

Step 2: Transformation & Cleaning
Some of the metadata tags extracted might contain malformed or escaped unicode sequences that break standard downstream JSON/CSV parsers (e.g., `\uXXXX` or weird custom delimiters). Write a Regex pattern in Go to sanitize these fields, stripping out any non-ASCII characters and invalid unicode escapes from the tags before further processing. 

Step 3: Deduplication
Perform hash-based deduplication on the packets. Two packets are considered duplicates if their `size` and `flags` are identical (regardless of timestamp). Maintain a registry of seen hashes (or composite keys) and discard duplicate packets from your final dataset. Keep only the first occurrence.

Step 4: Anomaly / Changepoint Detection
Process the deduplicated stream in chronological order (by `pts_time`). Detect "size anomalies". An anomaly is defined as any packet whose `size` is greater than 300% (i.e., strictly greater than 3.0 times) the size of the immediately preceding valid, deduplicated packet. The very first packet cannot be an anomaly.

Step 5: API Service
Your Go application must act as a long-running HTTP server listening on `127.0.0.1:8080`. It must expose the following endpoints:
1. `GET /api/stats`
   Returns a JSON object with:
   - `total_processed`: Integer count of raw packets extracted.
   - `total_deduplicated`: Integer count of unique packets remaining.
   - `total_anomalies`: Integer count of anomalies detected.
2. `GET /api/anomalies`
   Returns a JSON array of strings representing the `pts_time` of each detected anomaly, ordered chronologically.

Your server should remain running so that our automated test suite can query it. You can assume the video frame analysis runs either on startup or on the first request. Use only standard Go libraries where possible. Put your code in `/home/user/analyzer.go` and start the server.