You are an observability engineer tasked with tuning a monitoring pipeline. You need to build a robust data ingestion and analysis pipeline that processes incoming metric logs and correlates them with screen recordings of a legacy dashboard.

Your objectives:

1. **Pipeline Directory Setup:**
   Write an idempotent bash script at `/home/user/setup_pipeline.sh` that creates the following directory structure:
   - `/home/user/pipeline/logs/incoming/`
   - `/home/user/pipeline/logs/processed/`
   - `/home/user/pipeline/video_frames/`
   Ensure this script safely handles existing directories without failing.

2. **Log Sanitization (Adversarial Filter):**
   Incoming logs are JSON files, but some are corrupted or contain malicious injections. 
   Write a Python script at `/home/user/filter_logs.py` that takes two arguments: `<input_directory>` and `<output_directory>`. 
   The script must iterate through all `.json` files in the input directory. A file should be copied to the output directory ONLY if it meets ALL of the following criteria:
   - It is valid JSON.
   - It contains the keys: `timestamp`, `service_name`, and `cpu_usage`.
   - `cpu_usage` is a numeric value between 0 and 100 (inclusive).
   - `service_name` is a string that DOES NOT contain any of the following characters: `<`, `>`, `|`, `&`, `;`, `$`.
   Files failing these checks must be ignored.

3. **Dashboard Video Analysis:**
   A recording of the legacy dashboard is located at `/app/dashboard_recording.mp4`. We need to detect "critical alert" flashes.
   Write a Python script at `/home/user/analyze_video.py` that uses `ffmpeg` (via subprocess) or `cv2` (if installed) to analyze the video.
   The script must determine the total number of frames where the top-right 100x100 pixel quadrant has an average Red channel value strictly greater than 150, and average Green and Blue channel values strictly less than 50.
   The script should print this single integer count to stdout.

4. **Integration:**
   Write a master script at `/home/user/run_pipeline.sh` that:
   - Runs `setup_pipeline.sh`.
   - Runs `filter_logs.py` to process logs from `/app/corpus/mixed_logs/` (assume this exists during your run) and output them to `/home/user/pipeline/logs/processed/`.
   - Runs `analyze_video.py` and saves the integer output to `/home/user/pipeline/video_alert_count.txt`.

Ensure all scripts are executable.