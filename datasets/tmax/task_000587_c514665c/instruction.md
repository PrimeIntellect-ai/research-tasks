As an automation specialist, I need you to build a robust data processing workflow to handle our legacy time-series telemetry. 

First, we have a video file located at `/app/telemetry_dashboard.mp4`. This video contains a flashing warning light in the top-left 50x50 pixels. I need you to extract a time series representing the average red-channel intensity of that 50x50 region for every frame. Normalize this time series to a 0-1 scale and save it as a CSV file at `/home/user/video_telemetry.csv` with columns `frame_index` and `red_intensity`.

Second, we process thousands of historical telemetry logs stored in JSON-lines format. Our legacy ingestion system sometimes produces corrupted logs with malformed unicode escape sequences, duplicate timestamps, and noisy sensor values. I need you to write a sanitizer script (in a language of your choice) that reads a JSON-lines file from standard input and writes cleaned JSON-lines to standard output. 

Your sanitizer script must be located at `/home/user/sanitizer.sh` (or `.py`, etc., just ensure it is executable and can be run as `./sanitizer.sh < input.jsonl > output.jsonl`). 

The sanitizer must:
1. Handle and properly unescape or strip malformed unicode escape sequences that normally break standard JSON parsers.
2. Remove exact duplicate records.
3. Compute a similarity metric to identify and drop records that are too close in time (within 10 milliseconds of the previous valid record) as they are likely bounce-noise.
4. Preserve the exact structure of valid records.

Your script will be tested against two corpora:
- A "clean" corpus containing perfectly valid JSON-lines files. Your script must preserve these 100% unchanged (except for fixing deduplication/bounce-noise as defined above, though the clean corpus has none of these issues).
- An "evil" corpus containing heavily corrupted files with malicious unicode escapes and extreme bounce-noise. Your script must successfully parse, sanitize, and output only the valid reconstructed records without crashing.

Please create the extraction pipeline for the video and the sanitizer script.