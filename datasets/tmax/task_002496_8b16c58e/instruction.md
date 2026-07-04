We have a screen recording of our configuration manager's dashboard streaming log events, located at `/app/config_dashboard.mp4`. We lost the original text logs and need to reconstruct the configuration change metrics.

You need to accomplish two things:

1. **Write a Data Processing Program in Go**
Create a Go program at `/home/user/parser.go` that reads raw configuration log lines from `stdin` and outputs aggregated metrics to `stdout`.

Input format (space-separated, one per line):
`[TIMESTAMP] SERVER_ID ACTION KEY NEW_VALUE`
Example:
`[2024-03-15T10:23:45Z] web-01 UPDATE max_connections 500`

Requirements for the Go program:
- Parse the ISO8601 timestamps.
- Group the events into strict 15-minute time buckets (e.g., `2024-03-15T10:00:00Z` to `2024-03-15T10:14:59Z`, `2024-03-15T10:15:00Z` to `2024-03-15T10:29:59Z`).
- For each bucket and each `SERVER_ID`, calculate:
  - The total number of events.
  - The number of *unique* `KEY`s modified.
- Output the aggregated data as a strict CSV to `stdout` with the header:
  `BucketStart,ServerID,TotalEvents,UniqueKeys`
- The CSV output must be sorted chronologically by `BucketStart` (ascending), and then alphabetically by `ServerID` (ascending).
- Ignore any malformed lines that do not strictly match the 5-column format or have invalid timestamps.

2. **Process the Video**
Extract the text logs from `/app/config_dashboard.mp4`. The video shows clean, high-contrast monospace text of these logs (you can use `ffmpeg` and `tesseract` to extract the frames and text).
Once extracted, pipe the recovered log lines through your compiled Go program and save the output to `/home/user/video_summary.csv`.

Your Go program will be rigorously tested against a reference implementation with randomized log inputs to ensure perfect edge-case equivalence.