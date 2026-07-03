You are a data analyst tasked with building a reproducible ETL pipeline using strictly Bash and standard Linux CLI tools (like `awk`, `sed`, `ffmpeg`, and `imagemagick`). No Python, R, or other scripting languages are allowed for your data processing pipeline.

You have been provided with two data sources:
1. A video file of an industrial chemical reaction: `/app/reaction.mp4`
2. A messy raw sensor log: `/app/sensor_log.csv`

Your goal is to build a Bash-only pipeline that extracts visual features from the video, cleans the sensor data, joins them, and flags anomalies.

Follow these pipeline requirements:
1. **Video Feature Extraction**:
   - Extract exactly 1 frame per second from `/app/reaction.mp4`.
   - For each extracted frame, compute its average grayscale intensity on a 0-255 scale (you may use `imagemagick`/`magick`).

2. **Data Cleaning**:
   - Parse `/app/sensor_log.csv`. The file has columns: `time_sec`, `sensor_a`, `sensor_b`, `notes`.
   - Filter out any rows where `sensor_a` is explicitly the string `NULL` or empty.
   - Strip any leading/trailing whitespace from the remaining fields.

3. **Feature Engineering & Integration**:
   - Join the computed visual intensity for each second with the corresponding `time_sec` in the cleaned sensor log. (Assume frame 1 corresponds to `time_sec=1`, frame 2 to `time_sec=2`, etc.).
   - Create a derived boolean column `anomaly_flag`. Set it to `1` if the extracted visual intensity is strictly greater than 120 AND `sensor_a` is strictly greater than 45.0. Otherwise, set it to `0`.

4. **Output Validation**:
   - Write your final integrated dataset to `/home/user/results.csv`.
   - The file must be a valid CSV with exactly the following header: `time_sec,sensor_a,intensity,anomaly_flag`.
   - The data must be sorted numerically by `time_sec`.

Create a single executable bash script at `/home/user/pipeline.sh` that performs this entire workflow automatically when run. After writing the script, execute it to produce `/home/user/results.csv`.