You are a Data Engineer and Systems Analyst tasked with cleaning and validating an automated driving dataset. We have an integrated pipeline that involves processing dashcam video feeds, joining them with CSV telemetry data, and identifying data-leakage anomalies in external datasets. 

Your entire solution must be implemented in **Rust** (you may use standard bash utilities like `ffmpeg` to assist, but the core joining, schema enforcement, outlier handling, and anomaly detection must be written in Rust).

**Phase 1: Video and Telemetry Fusion**
You have a video file located at `/app/dashcam.mp4` recorded at exactly 10 frames per second. 
1. Extract the frames from this video.
2. For each frame, compute the average grayscale brightness (0-255).
3. Read the base telemetry dataset at `/app/telemetry_base.csv`. This file contains `timestamp` (in seconds), `speed`, and `steering` columns. There are some missing values (NaN/null) in the `speed` column, which you must interpolate linearly. 
4. Join the video frame brightness to the telemetry data. Match each frame's timestamp (e.g., frame 0 = 0.0s, frame 1 = 0.1s, etc.) with the closest telemetry timestamp. 
5. Output the strictly typed, schema-enforced joined data to `/home/user/video_joined.csv` with columns: `timestamp`, `speed` (interpolated), `steering`, `brightness`.

**Phase 2: Adversarial Data Leak Detector**
We continuously receive normalized datasets from a third-party vendor, but we suspect their data science team is making a classic "fit_transform" mistake: scaling data using global statistics (which leaks future data into past features) rather than causal, rolling statistics.
We have provided a training corpus:
- `/app/corpus/clean/`: Contains 20 CSV files where the `sensor_scaled` column was correctly normalized using a rolling window (only past data).
- `/app/corpus/evil/`: Contains 20 CSV files where the `sensor_scaled` column was improperly normalized using the global mean/std of the entire file (future data leaked).

Your job is to create a Rust CLI tool that detects this data leak mathematically (using your linear algebra and statistical skills to reverse-engineer if future data influenced the current row).
Create a Rust binary that compiles to `/home/user/detector`.
- It must accept a single argument: the path to a CSV file.
- It must analyze the file, and exit with code `0` if the file is cleanly generated (no forward leak), and exit with code `1` if it is "evil" (leaked).

**Phase 3: Experiment Tracking**
Log your summary statistics to `/home/user/experiment_log.json`. It must contain:
- `video_frames_processed`: integer count of frames.
- `max_brightness`: float of the highest average frame brightness.
- `missing_speeds_imputed`: integer count of NaN speed rows you interpolated.

**Constraints:**
- Use Rust for the detector and the data joining logic. You may create a Cargo project in `/home/user/pipeline`.
- Do not hardcode the validation against the specific files in the corpus; your detector must generalize to hidden files generated with the same mathematical anomaly.