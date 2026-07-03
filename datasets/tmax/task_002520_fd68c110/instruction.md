You are an automation specialist tasked with recovering and reconstructing a corrupted sensor data pipeline. 

A critical monitoring system failed, leaving us with a partially corrupted JSON-lines log file and an emergency audio backup containing the missing data points encoded in International Morse Code. You must build a Python pipeline to recover the full dataset, resample it, and compare it against a partial reference model.

**Inputs:**
1. `/app/sensor_logs.jsonl`: A JSON-lines file containing timestamps (ISO 8601) and sensor readings (float). Due to a logging bug, several lines contain broken Unicode escape sequences (e.g., `\u001` instead of `\u001a`) causing standard JSON parsers to crash.
2. `/app/backup_morse.wav`: A WAV file containing the missing data points. The data is encoded as International Morse Code using a 1000 Hz sine wave tone. Format: `<HHMM> <VALUE>`, separated by spaces. Example decoded text: `1205 45.2 1215 48.1`. 
3. `/app/reference.csv`: A CSV containing expected baseline values at 5-minute intervals.

**Your Pipeline Must:**
1. **Parse & Clean:** Extract all valid `timestamp` and `value` pairs from the JSONL file. Gracefully skip or repair the lines with broken Unicode.
2. **Decode Audio:** Write a custom Python routine (using signal processing, distance/similarity computation, or template matching) to decode the Morse code in `/app/backup_morse.wav`. 
3. **Merge & Aggregate:** Combine the JSONL data with the decoded audio data (assume the audio dates match the JSONL date of `2023-10-01`). Aggregate the combined data into 5-minute time buckets (e.g., `12:00:00`, `12:05:00`). If a bucket has multiple values, take the mean.
4. **Resample & Gap-Fill:** Create a continuous time series from `2023-10-01 12:00:00` to `2023-10-01 13:00:00` at exactly 5-minute intervals. Use linear interpolation to fill any remaining gaps.
5. **Log & Monitor:** Your script must maintain a log at `/home/user/pipeline.log`. It should log:
   - `[INFO] Parsed X valid records from JSONL`
   - `[INFO] Decoded audio: <recovered_string>`
   - `[INFO] Pipeline completed.`
6. **Compare:** Compute the Mean Squared Error (MSE) between your final reconstructed time series values and the values in `/app/reference.csv` (ensure both are aligned by time).
7. **Output:** Save your final computed MSE as a single float value in a file located at `/home/user/mse_result.txt`.

Ensure your Python code is robust, well-structured, and executes the entire ETL and recovery workflow.