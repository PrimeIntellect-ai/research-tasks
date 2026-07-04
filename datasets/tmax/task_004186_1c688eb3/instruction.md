You are an automation specialist managing an ETL pipeline that processes video feeds into a time-series database. The current pipeline frequently produces duplicate records upon retry due to overlapping frame extractions.

Write a Python script at `/home/user/video_etl.py` that processes a video file and generates idempotent SQL insert statements.

Initial logic and parameters are validated:
- Accept an MP4 video file path as the first command-line argument.
- Extract frames at exactly 1 frame per second (FPS) using a deterministic method (e.g., converting to grayscale rawvideo).
- Calculate the mean grayscale brightness (0-255) of each frame.
- Normalize this brightness to a float between 0.000 and 1.000.

Apply time-based bucketing and template-based text generation to finalize the output:
- Group frames into 5-second tumbling windows (e.g., [0-4], [5-9]).
- Output exactly one SQL statement per window to standard output, incorporating an UPSERT strategy to resolve retry duplicates.

Final required transformation format (print exactly this to stdout for each window):
`INSERT INTO video_metrics (window_start, window_end, avg_brightness) VALUES ({start}, {end}, {avg}) ON CONFLICT (window_start) DO UPDATE SET avg_brightness = EXCLUDED.avg_brightness;`
Where `{avg}` is rounded to exactly 3 decimal places.