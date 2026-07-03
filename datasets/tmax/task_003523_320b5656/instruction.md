You are an automation specialist for a smart manufacturing facility. Your task is to build a time-series data integration pipeline that processes real-time video telemetry and merges it with external sensor data. 

We have two primary data sources:
1. A video feed of a conveyor belt, located at `/app/conveyor.mp4`.
2. A directory of raw sensor logs, which unfortunately contains a mix of clean and heavily corrupted (adversarial/malformed) data.

Your objective is to complete the following multi-stage workflow:

**Step 1: Video Telemetry Extraction**
Use `ffprobe` (part of the ffmpeg suite) to extract a time series of frame packet sizes from `/app/conveyor.mp4`.
Extract the `pkt_pts_time` (timestamp) and `pkt_size` (size in bytes) for every video frame. Save this as a CSV file named `/home/user/video_ts.csv` in the format: `timestamp,size`.

**Step 2: C-based Time-Series Filter (Quality Gate & Deduplication)**
You must write a C program, `/home/user/ts_filter.c`, and compile it to `/home/user/ts_filter`.
This program will act as a strict sanitization filter for the sensor logs. It must:
- Accept a single command-line argument: the path to a sensor log CSV file.
- Read the file line by line. The expected schema is `timestamp,sensor_id,value`.
- **Validation Checkpoint**: Drop any line where `timestamp` or `value` cannot be parsed as a valid float, or if the line does not have exactly three comma-separated fields.
- **Hash-based Deduplication**: Track seen timestamps (you may use a simple hash set or fixed array, assuming no more than 10,000 unique timestamps per file). If a timestamp has already been encountered in the file, drop the duplicate row (keep the first occurrence).
- Output the sanitized, deduplicated rows to standard output (`stdout`) in the exact same `timestamp,sensor_id,value` format.
- Exit with code 0.

*Note on testing:* The system contains two corpora to test your C program:
- `/app/corpora/clean/`: Contains perfectly formatted sensor data. Your filter MUST preserve these files 100% unchanged.
- `/app/corpora/evil/`: Contains malformed lines, duplicated timestamps, and string injections. Your filter MUST strictly sanitize these, dropping all invalid or duplicate rows without crashing.

**Step 3: Integration (Join/Merge)**
Write a shell script `/home/user/pipeline.sh` that takes a sensor log file as an argument. The script should:
1. Run your `ts_filter` on the provided sensor log.
2. Join the sanitized sensor output with `/home/user/video_ts.csv` on the `timestamp` column (assume exact matching for this scenario; you can use `join`, `awk`, or any standard Linux tool).
3. Print the joined result in the format `timestamp,sensor_id,value,size`.

Ensure your C code is robust and your pipeline script is executable. You do not need to run the verifier yourself, but you must ensure your tools perfectly conform to the clean/evil specifications.