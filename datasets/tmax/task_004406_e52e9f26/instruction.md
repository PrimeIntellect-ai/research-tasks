You are an assistant helping a data scientist fix a broken data processing pipeline. 

We have a daily feed of IoT sensor readings in a CSV file located at `/home/user/data/sensors.csv`. Currently, the pipeline is dropping records. The data scientist wrote a naive Go script at `/home/user/process.go` that reads the file line-by-line using `bufio.Scanner` and splits strings by commas. However, the `notes` column in our CSV often contains quoted embedded newlines (e.g., `"Calibration\nRestart"`), which causes the naive scanner to break lines incorrectly and drop data silently.

Your task is to fix and enhance the Go script (`/home/user/process.go`) to achieve the following:
1. **Robust CSV Parsing**: Correctly parse the CSV handling embedded newlines.
2. **Sorting and Grouping**: Group the records by `sensor_id` and sort each group chronologically by `timestamp` (integer).
3. **Imputation (Interpolation)**: Some rows have an empty `temperature` field. You must perform linear interpolation to fill these missing values. If a value is missing, it should be the exact midpoint between the nearest valid chronologically prior and subsequent temperatures for that sensor. (Assume missing values will never occur at the very beginning or end of a sensor's time series, and you won't have two consecutive missing values).
4. **Windowed Aggregation**: For each record, calculate a rolling 3-reading moving average of the `temperature` (including the current reading and up to 2 previous readings for that sensor). If fewer than 3 readings are available so far, average the available ones.
5. **Output Formatting**: Write the results to `/home/user/output.jsonl`. Each line must be a valid JSON object with the following schema:
   `{"timestamp": 100, "sensor_id": "S1", "temperature": 20.0, "moving_avg": 20.0}`
   *Note: Format floating-point numbers to exactly 2 decimal places before adding to the JSON, or represent them as standard JSON numbers if using a struct, but ensure accuracy to 2 decimal places.*

Finally, to schedule this pipeline, create a crontab entry file at `/home/user/crontab.txt` that schedules `go run /home/user/process.go` to run every 15 minutes, every day, every month, every day of the week.

Ensure your code is compiled or run successfully so that `/home/user/output.jsonl` and `/home/user/crontab.txt` exist and contain the correct values.