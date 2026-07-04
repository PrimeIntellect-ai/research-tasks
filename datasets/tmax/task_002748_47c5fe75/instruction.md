You are acting as a data scientist cleaning up a multimodal dataset containing traffic video recordings and telemetry logs. We need to build a robust data processing pipeline in Rust that handles anomaly detection and video analysis.

There are two main objectives:

### 1. Telemetry Log Sanitization (Adversarial Filtering)
We receive telemetry logs in JSON format. Unfortunately, some logs contain data corruption, physically impossible values, or malicious template injections in the metadata. 
You must write a Rust CLI tool that reads a directory of JSON log files, filters them, and writes the valid ones to an output directory. 

Each JSON log looks like this:
`{"timestamp": 1670000000, "device_id": "sensor_A", "speed_mps": 25.0}`

A log is "evil" (invalid) and must be discarded if:
- `device_id` contains the characters `<` or `>` or `{` or `}` (preventing template injection).
- The `speed_mps` is negative.
- The `speed_mps` exceeds 100.0.

Your tool must be a Rust binary project located at `/home/user/log_filter`.
It must accept exactly two arguments: input directory and output directory.
Example: `cargo run --release -- <input_dir> <output_dir>`
The tool should iterate over all `.json` files in the input directory, process each line (assuming JSONL or one JSON object per file), and write the valid JSON files to the output directory (keeping the original filename).

### 2. Video Activity Detection (Time-based bucketing & Rolling Aggregation)
We have a traffic camera recording located at `/app/traffic.mp4`.
Using `ffmpeg` and Rust, you must:
1. Extract frames from `/app/traffic.mp4` at 1 frame per second.
2. Write a Rust program (can be in the same cargo workspace, e.g., `/home/user/video_analyzer`) that reads the extracted frames.
3. Compute a rolling difference: for each second `t`, compute the absolute difference in file size between the JPEG frame at `t` and `t-1`. 
4. Apply a tumbling time-based bucket of 5 seconds. For each 5-second window (0-4, 5-9, etc.), calculate the sum of the rolling differences.
5. Generate a Markdown report at `/home/user/report.md` using a simple text template. The report must contain:
   - Pipeline monitoring log (e.g., "Processed X frames").
   - A list of the 5-second windows and their aggregated differences.

Format of `/home/user/report.md`:
```
# Traffic Analysis Report
Processed [Total Frames] frames.

## Activity by 5-second Window
- Window 0-4s: [Sum] bytes
- Window 5-9s: [Sum] bytes
...
```

Ensure your Rust code uses standard error handling and pipeline logging (print statements are fine). Do not use external libraries for the core filtering or math logic (serde for JSON is allowed).