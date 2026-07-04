You are a Machine Learning Engineer tasked with preparing a training dataset for a lightweight heuristic model that predicts vehicle behavior based on visual complexity, sensor telemetry, and weather conditions. 

You have been given a raw video and two scattered metadata files. You need to build a Bash-based ETL (Extract, Transform, Load) pipeline to join and aggregate these multimodal data sources. 

Here are the input files provided in the container:
1. `/app/dashcam.mp4`: A short dashcam video recording.
2. `/app/sensor_data.txt`: Pipe-separated telemetry data. 
   Format: `time_sec | speed_kmh | steering_angle`
3. `/app/weather.csv`: Comma-separated weather data. 
   Format: `time_sec,condition,temp_celsius`

**Objective 1: Data Joining & Aggregation Script**
Create a Bash script at `/home/user/generate_row.sh` that takes a single integer argument `T` (representing a timestamp in seconds).
The script must perform the following steps using only standard Bash, coreutils, and `ffmpeg`/`ffprobe`:
1. **Video Transformation (Visual Complexity Metric):** Use `ffprobe` to extract the packet sizes of the video stream (`v:0`). Calculate the sum of the sizes (in bytes) of all video packets whose presentation timestamp (`pts_time`) is greater than or equal to `T`, and strictly less than `T + 1`. If there are no packets in that range, the sum should be `0`.
2. **Multi-source Data Joining:** 
   - Extract the `speed_kmh` from `/app/sensor_data.txt` where `time_sec` exactly matches `T`.
   - Extract the `temp_celsius` from `/app/weather.csv` where `time_sec` exactly matches `T`.
3. **Output Format:** Print exactly one comma-separated line to standard output in this format:
   `T,sum_bytes,speed_kmh,temp_celsius`

*(Example: If T=2, sum=145000, speed=45, temp=22.5, output should be `2,145000,45,22.5`)*

**Objective 2: Inference Benchmarking**
To ensure the pipeline is performant enough for real-time training loop generation, create a benchmarking script at `/home/user/benchmark.sh`.
This script must:
1. Run `/home/user/generate_row.sh T` sequentially for `T` from `0` to `5` inclusive.
2. Discard the standard output of those runs.
3. Measure the total real wall-clock time taken to execute all 6 runs combined.
4. Output *only* the total execution time (in seconds, e.g., `1.45`) to a log file at `/home/user/benchmark.log`.

Make sure `/home/user/generate_row.sh` is executable (`chmod +x`). 
Do not use Python or other scripting languages; stick to standard Unix tools (awk, grep, sed, etc.) and `ffprobe`/`ffmpeg`.