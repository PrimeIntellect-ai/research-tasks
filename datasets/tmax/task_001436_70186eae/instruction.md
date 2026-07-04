You are a data engineer tasked with building a Bash-only ETL pipeline to analyze a scientific video experiment. A video artefact is located at `/app/experiment.mp4`.

You must implement an ETL pipeline that extracts frame-level statistics, enforces a specific schema, engineers sequential features, and performs a statistical bootstrap estimation—using only standard Linux CLI tools (Bash, awk, sed, grep, bc, jq, etc.) and `ffmpeg` (which is preinstalled). Do not use Python, R, or other scripting languages.

Your pipeline should be written as a reusable shell script at `/home/user/pipeline.sh` that takes the video file path as its first argument.

Here is the specification for your pipeline:

1. **Feature Extraction:**
   Use `ffmpeg` to process the input video and extract the average luma (YAVG) for each frame. 
   *(Hint: You can use the `signalstats` video filter and parse the standard error output).*

2. **Data Schema Enforcement & Feature Engineering:**
   Construct a CSV dataset and save it to `/home/user/features.csv`.
   The CSV must have the following header exactly: `frame_index,luma_avg,delta_luma`
   - `frame_index`: Integer starting at 0 for the first frame.
   - `luma_avg`: The extracted YAVG value for that frame (keep the original precision).
   - `delta_luma`: The difference in `luma_avg` from the *previous* frame (i.e., `luma_avg[n] - luma_avg[n-1]`). For `frame_index` 0, set `delta_luma` to `0`.

3. **Data Filtering:**
   Filter out any frames from your dataset where `luma_avg` is strictly less than `50.0`. Keep the remaining valid frames for the next step.

4. **Statistical Bootstrapping:**
   Using pure Bash and/or `awk`, implement a bootstrap routine to estimate the expected value of `delta_luma` from the filtered dataset.
   - Generate `B=1000` independent bootstrap samples. Each bootstrap sample is created by sampling with replacement from the filtered `delta_luma` values until you reach the same count as the filtered dataset.
   - Calculate the mean of `delta_luma` for each bootstrap sample.
   - Finally, compute the grand mean of those 1000 bootstrap means.
   
5. **Output Requirement:**
   Save the final estimated grand mean as a single floating-point number in `/home/user/bootstrap_result.txt`.

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`) and that you run it successfully on `/app/experiment.mp4` to produce both `/home/user/features.csv` and `/home/user/bootstrap_result.txt`. Your bootstrap implementation will be tested against a numeric threshold.