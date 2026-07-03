You are a data analyst analyzing a drone sensor package. The drone provides a video feed of its flight and a basic, but unreliable, telemetry log.

Your objective is to build a bash-based data processing pipeline that merges visual data with telemetry and provides an aggregation query tool.

You have two initial artifacts:
1. A video file located at `/app/drone_feed.mp4` (exactly 120 seconds long).
2. A gappy CSV file located at `/home/user/data/telemetry.csv` with columns `timestamp,speed`. Timestamps are integers representing seconds (1 to 120). Due to sensor dropouts, many timestamps are completely missing.

**Step 1: Video Feature Extraction**
Use `ffmpeg` to extract exactly one frame per second from `/app/drone_feed.mp4`. Extract them as JPEG images. 
Calculate the file size (in bytes) of each frame. This byte size will serve as our proxy for "visual complexity" for that second.

**Step 2: Imputation and Gap-Filling**
Process the `telemetry.csv` file. You must generate a complete timeline from second 1 to 120.
- If a timestamp is missing a speed value, you must impute it using **forward-fill** (carry forward the last known speed). 
- If timestamp 1 is missing, assume a default starting speed of `0.0`.
- All speeds should be treated as floating-point numbers.

**Step 3: Query Tool**
Write a Bash script at `/home/user/query_range.sh` that takes exactly two integer arguments: `<start_sec>` and `<end_sec>`.
When executed like `./query_range.sh 15 45`, the script must:
1. Look at the inclusive range between `start_sec` and `end_sec`.
2. Compute the **average speed** over that range (using your imputed data), rounded to exactly one decimal place.
3. Compute the **maximum frame size** (in bytes) among the extracted frames in that same time range.
4. Output the result to standard out in this exact format:
   `AverageSpeed: <val> | MaxFrameSize: <val>`

**Rules and Constraints:**
- Use Bash, standard coreutils (e.g., `awk`, `sed`, `grep`, `xargs`), and `ffmpeg`. Do not write Python, Ruby, or Perl scripts.
- Your script `/home/user/query_range.sh` must be executable (`chmod +x`).
- Your script must run efficiently, as it will be fuzzed hundreds of times by our automated test suite with random timestamp ranges.
- Do not make assumptions about the data beyond what is specified; build a robust multi-stage pipeline.