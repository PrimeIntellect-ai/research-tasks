You are a data analyst working with drone flight telemetry and onboard video feeds. You need to build a robust data processing pipeline in Go that handles CSV stream filtering, video feature extraction, and dataset merging. 

We have a raw telemetry feed and a synchronized onboard video file. However, the telemetry feed is known to contain corrupted or malicious records due to transmission errors, and we must rigorously filter these out.

Your task is to implement an ETL pipeline with the following requirements:

1. **Telemetry Filter (Adversarial Validation Checkpoint):**
   Write a Go program (source at `/home/user/filter.go`) that can be built into a CLI tool named `telemetry_filter`. 
   The tool must read a CSV from `stdin` and print the validated, cleaned CSV to `stdout`.
   - **Schema:** `timestamp_sec,latitude,longitude,altitude,status`
   - **Validation Rules:**
     - `timestamp_sec` must be a valid non-negative integer.
     - `latitude` must be a valid float between -90.0 and 90.0 inclusive.
     - `longitude` must be a valid float between -180.0 and 180.0 inclusive.
     - `altitude` must be a float greater than or equal to 0.0.
     - `status` must be exactly one of: "OK", "WARN", "ERR".
     - Any row failing *any* of these rules, or having an incorrect number of columns, must be silently dropped.
     - The output must preserve the exact header: `timestamp_sec,latitude,longitude,altitude,status`.

2. **Video Feature Extraction:**
   An onboard video file is provided at `/app/drone_flight.mp4`.
   Using `ffmpeg` and Go, extract the frames at 1 frame per second (starting at timestamp 0).
   For each extracted frame, calculate the average grayscale brightness (an integer from 0-255). The standard luminance formula is not strictly required; you may simply average all RGB channels or use ffmpeg's grayscale conversion and average the pixel values.
   Output this data to a CSV file at `/home/user/video_features.csv` with the header:
   `timestamp_sec,brightness`

3. **Pipeline Integration:**
   Write a bash script `/home/user/pipeline.sh` that orchestrates the DAG:
   - Compiles the Go filter.
   - Runs `telemetry_filter` on the primary raw feed located at `/app/raw_telemetry.csv` and saves the output to `/home/user/clean_telemetry.csv`.
   - Runs your video feature extraction logic to produce `/home/user/video_features.csv`.
   - Merges the two generated files on the `timestamp_sec` column (inner join) using Go, bash, or any standard Linux tool (like `join`).
   - The final merged file must be saved to `/home/user/merged_output.csv` with the header: `timestamp_sec,latitude,longitude,altitude,status,brightness`. 
   - Ensure your script exits with code 0 on success.

You may use standard Go library packages. `ffmpeg` is pre-installed on the system.