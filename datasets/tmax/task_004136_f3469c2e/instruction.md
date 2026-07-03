You are acting as a data engineer assisting a data science team. We have a continuous stream of noisy sensor data that needs to be cleaned, validated, and normalized before downstream analysis. 

We received the dataset cleaning parameters in a scanned document located at `/app/sensor_config.png`. 

Your objectives are:

1. **Parameter Extraction (OCR & Parsing):**
   Extract the configuration parameters from the image `/app/sensor_config.png`. You will find three key configuration values:
   - `W_SIZE`: The window size for the rolling statistics.
   - `THRESH_MULT`: The multiplier used for anomaly detection.
   - `FMT`: The specific string template to use for output generation.

2. **Stream Processing Script (`/home/user/stream_cleaner.py`):**
   Write a Python script that reads JSON Lines (JSONL) from `sys.stdin` and writes formatted text to `sys.stdout`.
   - **Validation Checkpoint:** For each line, parse the JSON. If a line is invalid JSON, missing required fields (`sensor_id`, `timestamp`, `value`), or if `value` cannot be cast to a float, silently drop the line (quality gate).
   - **Rolling Statistics:** For each `sensor_id`, maintain a sliding window of the last `W_SIZE` valid values (including the current value). Calculate the rolling simple moving average (`mean`). If fewer than `W_SIZE` values are available for a sensor, calculate the mean using all available historical values for that sensor.
   - **Anomaly Detection:** Determine the `status` of the current reading. If `abs(value - mean) > (THRESH_MULT * mean)`, the status is `"ANOMALY"`. Otherwise, it is `"OK"`.
   - **Template-Based Generation:** Format the output using the exact `FMT` string extracted from the image. You should format `mean` to exactly 2 decimal places.
   - **Parallel/Independent Processing Constraint:** The logic must independently track the state for each `sensor_id`. The output lines must be printed in the *exact same order* as the valid input lines were received.

3. **Pipeline Scheduling:**
   Create a bash wrapper script at `/home/user/pipeline.sh` that executes: `cat /home/user/data.jsonl | python3 /home/user/stream_cleaner.py > /home/user/cleaned_output.txt`. 
   Configure the user's crontab to run this wrapper script every 5 minutes.

Ensure your `stream_cleaner.py` strictly reads from standard input and prints to standard output, as it will be rigorously tested against an automated fuzzer providing a variety of interleaved sensor data streams.