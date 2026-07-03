You are a log analyst investigating network patterns that have been encoded into a video file for visual monitoring.

Your task is to build a data pipeline that extracts the encoded logs, deduplicates them, computes rolling statistics, and serves the results via an HTTP API.

1. **Extract and Deduplicate:**
   - Read the video file located at `/app/traffic_monitor.mp4`.
   - Extract frames at exactly 1 frame per second as PNG images using `ffmpeg`.
   - Perform hash-based deduplication: compute the MD5 hash of each PNG file. If multiple consecutive frames have the identical MD5 hash, keep only the first one and discard the rest.

2. **Compute Brightness:**
   - For each unique frame (in chronological order), calculate the average pixel brightness. Convert the image to grayscale (if not already), sum all pixel values (0-255), and divide by the total number of pixels.

3. **Windowed Aggregation:**
   - Apply a rolling average with a window size of 3 to the sequence of average brightness values. (For the first element, the rolling average is just the element itself. For the second, it's the average of the first two. From the third onwards, it's the average of the current and two previous values).

4. **Serve Summary Statistics:**
   - Compute the overall minimum, maximum, and average of these rolling averages.
   - Start an HTTP server listening on `0.0.0.0:8080`.
   - When a `GET` request is made to `/stats`, it must return a JSON response in exactly this format (values rounded to 2 decimal places):
     `{"min": 12.34, "max": 234.56, "avg": 123.45}`

5. **Pipeline Scheduling:**
   - Create a crontab configuration file at `/home/user/pipeline.cron` that schedules a hypothetical script `/home/user/process.sh` to run every 5 minutes. 
   - You don't need to actually start the cron daemon, just place the correctly formatted file there.

Write the necessary scripts (you may use Python, Bash, or any standard Linux tools) and leave the HTTP server running in the background or foreground.