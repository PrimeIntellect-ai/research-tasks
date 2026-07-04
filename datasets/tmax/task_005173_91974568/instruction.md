You are a data analyst tasked with processing a large batch of sensor data from our edge servers. 

We have a massive CSV file located at `/home/user/sensor_data.csv`. The file is encoded in UTF-16LE and has the following columns:
`timestamp,sensor_id,component,value`

The components are `CPU`, `MEM`, and `DISK`.
We need to detect anomalous readings. However, the baseline values for each component were left in an audio message by the lead engineer before they went on vacation.

You will find the voicemail at `/app/thresholds.wav`. 

Your objectives:
1. Transcribe the audio file to extract the baseline values for CPU, MEM, and DISK. (You may use standard CLI tools, install a local transcriber like `whisper-cli`, or use any API you have access to).
2. Convert the CSV file to standard UTF-8.
3. Process the CSV using standard shell utilities (e.g., `awk`, `bash`, `split`, `xargs`). To do this efficiently, you should implement parallel data processing.
4. Anomaly Detection Rule: A reading is considered an anomaly if its `value` is strictly greater than `(baseline_value * 1.5)`.
5. Extract the `timestamp` and `sensor_id` of all anomalous readings and save them to `/home/user/anomalies.csv` in the format: `timestamp,sensor_id`.

Your final output `/home/user/anomalies.csv` will be evaluated using a grading script that calculates the F1-score of your detected anomalies against our hidden ground truth. You must achieve an F1-score of at least 0.95.