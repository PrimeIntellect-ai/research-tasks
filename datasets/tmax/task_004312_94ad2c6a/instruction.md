You are acting as a localization engineer. We have an automated ETL pipeline that processes UI test videos to extract and update translation string metadata. Recently, the ETL job failed and its retry logic caused it to output duplicate and overlapping localization records. 

You have been provided with:
1. A video artifact at `/app/ui_test.mp4`. This video shows a sequence of translated UI screens. Each screen is displayed for exactly 5 seconds, separated by a 1-second black screen transition. 
2. A raw, corrupted ETL output file at `/home/user/raw_translations.jsonl`. This file contains JSON objects with keys: `timestamp` (seconds), `loc_key`, and `text`. Because of the retry bug, there are multiple duplicate entries for the same `loc_key` within the same UI screen display window, and their timestamps are jittered.

Your objectives:
1. **Analyze the Video**: Use `ffmpeg` to extract frames from `/app/ui_test.mp4` at 1 frame per second. Compute the mean pixel intensity (brightness) of each frame. Use a rolling window aggregation to detect the exact start and end seconds of each UI screen (a screen is "active" when the frame is not black, i.e., average brightness > 10).
2. **Deduplicate the ETL Data**: Read `/home/user/raw_translations.jsonl`. Group the records using time-based bucketing derived from the video analysis (match the `timestamp` of the record to the active screen windows). For each screen window, consolidate all records. If multiple records exist for the same `loc_key` in a single window, keep the one with the longest `text` (using string length as a proxy for the complete, non-truncated extraction) and discard the duplicates.
3. **Serve the Data**: Write a Python HTTP server listening on `127.0.0.1:8080`. 
   - Endpoint `GET /stats`: Return a JSON object with `{"total_unique_screens": X, "total_deduplicated_records": Y}`.
   - Endpoint `GET /data`: Return a JSON array of the deduplicated records, sorted by `timestamp` ascending.

Ensure your Python HTTP server is running continuously in the background so it can be tested. Write your deduplication logic in Python.