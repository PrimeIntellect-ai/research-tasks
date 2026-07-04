You are an automation specialist tasked with building a video-based telemetry extraction and anomaly detection pipeline. 

A diagnostic system records an indicator light panel and outputs video files. We have provided a sample video at `/app/telemetry.mp4`. Your goal is to extract a time series of brightness values from this video, and create a robust, reusable Python tool to detect changepoints and anomalies in any such time series.

**Step 1: Video Data Extraction (Pipeline Logging & Regex)**
Use `ffmpeg` with the `signalstats` filter to analyze `/app/telemetry.mp4`. Extract the `Yavg` (average luma/brightness) value for each frame. 
You must parse the text output of `ffmpeg` to construct a CSV-formatted stream. The expected CSV format is:
`frame_number,metric_name,value`
(e.g., `1,YAVG,142.5`). Note that `metric_name` should literally be the string `YAVG`.

**Step 2: The Anomaly Detector CLI (Validation, Anomaly Detection, Aggregation)**
Write a Python script at `/home/user/detector.py` that reads the CSV format from `standard input` (`stdin`) and processes it sequentially. 

The script must strictly adhere to the following rules so it can be automatically verified against our test suites:
1. **Validation Checkpoint:** Each line from stdin must be validated using a Regular Expression. The line must exactly match the format: an integer, a comma, a metric name (only uppercase/lowercase letters), a comma, and a numeric value (integer or decimal). 
   - If a line fails this validation, write exactly `[ERROR] Invalid line: <the_raw_line>` to `stderr` and skip it.
2. **Anomaly Detection:** For each valid metric name, maintain a rolling history of the most recent 3 valid values (excluding the current value). 
   - If there are fewer than 3 history values for a metric, do not perform detection, just add the current value to the history.
   - If there are 3 history values, calculate their exact mean. 
   - If the absolute difference between the current value and the mean is strictly greater than `15.0`, flag it as an anomaly.
   - When an anomaly is detected, print to `stdout`: `ANOMALY at frame <frame_number>: <metric_name> = <value_formatted_to_2_decimals> (avg = <mean_formatted_to_2_decimals>)`
   - *Important:* Do NOT include anomalous values in the rolling history. The rolling history should only contain the last 3 *normal* (non-anomalous) values.
3. **Summary Statistics:** When the input stream ends (EOF), print a summary to `stdout` starting with exactly `SUMMARY:` on its own line. Then, for each metric name encountered (sorted alphabetically), print `<metric_name>: <total_anomalies_detected>`.

**Step 3: Execution**
Once your script is ready, run your pipeline by piping the parsed `ffmpeg` CSV data directly into `/home/user/detector.py`, saving the standard output to `/home/user/final_report.txt` and standard error to `/home/user/pipeline_errors.log`.

*Constraint Checklist & Confidence Score:*
1. Parse ffmpeg output with regex? Yes.
2. Validation checkpoint (regex on detector input)? Yes.
3. Pipeline stderr/stdout logging? Yes.
4. Anomaly detection (rolling mean)? Yes.
5. Summary stats? Yes.