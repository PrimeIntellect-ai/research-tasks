You are an MLOps engineer processing experimental data. We have a visual sensor feed and a separate telemetry dataset that need to be fused, cleaned, and logged for experiment tracking.

There are two parts to this task: extracting the visual data and building the generalized fusion pipeline.

**Part 1: Video Signal Extraction**
We have an experiment dashboard video located at `/app/experiment_video.mp4` recorded at exactly 10 Frames Per Second (FPS).
The visual "sensor" signal we need to track is the average grayscale pixel intensity of the top-left 50x50 pixel region (x from 0 to 49, y from 0 to 49) in each frame.
Write a script to extract this signal and save it to `/home/user/video_signal.csv` with the headers `time` (in seconds, starting at 0.0) and `video_val`.

**Part 2: The Fusion & Tracking Pipeline**
You must write a general-purpose Python pipeline script at `/home/user/fusion_pipeline.py` that takes raw video signal CSVs, raw telemetry CSVs, cleans the data, and logs the experiment metrics.

Your script must accept the following command-line arguments:
`--video_in` (path to video signal CSV)
`--telemetry_in` (path to telemetry CSV, which contains `time` and `telemetry_val`)
`--out_csv` (path to output the cleaned, merged dataset)
`--out_log` (path to output the experiment tracking JSON)
`--window` (integer, rolling median window size)
`--threshold` (float, outlier threshold)

The script must perform the following data science operations in exact order:
1. **Join**: Perform an outer join on the `time` column. Assume times are aligned to 1 decimal place. Sort the merged dataset strictly by `time` ascending.
2. **Missing Values**:
   - For `telemetry_val`, use forward-fill for missing values. If there are missing values at the very beginning, use backward-fill for those remaining.
   - For `video_val`, use linear interpolation for missing values. Assume no `NaN` at the exact start or end (the fuzzer will guarantee bounding data points).
3. **Outlier Rejection**: Iterate through `video_val` and replace outliers with the rolling median.
   - Calculate a *centered* rolling median using the specified `--window` (which will always be an odd integer).
   - If `abs(video_val - rolling_median) > threshold`, count this as an anomaly and replace `video_val` with the `rolling_median`.
   - *Note*: For the first and last `window//2` elements where a centered window cannot be fully formed, do NOT perform outlier rejection (keep original values).
4. **Experiment Metrics**: Compute the Pearson correlation coefficient between the cleaned `video_val` and `telemetry_val`.

**Output Formats**:
- The script must write the cleaned joined data to `--out_csv` with exactly three columns: `time,video_val,telemetry_val`. All float values must be formatted to exactly 4 decimal places.
- The script must write a JSON file to `--out_log` with exactly two keys:
  - `"correlation"`: The Pearson correlation as a float rounded to 4 decimal places.
  - `"outliers_replaced"`: An integer count of how many `video_val` outliers were replaced.

*Note*: We will test your script `/home/user/fusion_pipeline.py` against thousands of randomly generated inputs to ensure your mathematical logic and data-handling rules match our rigorous expectations exactly.