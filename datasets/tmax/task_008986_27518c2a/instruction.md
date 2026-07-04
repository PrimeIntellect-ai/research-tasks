You are a data scientist working with a batch of messy sensor logs. You need to write a Bash script to clean, normalize, and extract information from these logs into a structured CSV format.

Your task is to create a Bash script at `/home/user/clean_data.sh` that processes a text file located at `/home/user/sensor_logs.txt` and outputs a clean CSV file at `/home/user/clean_sensors.csv`.

Here are the requirements for the processing pipeline:
1. **Extraction**: Each valid log line contains a sensor ID (e.g., `Sensor-A1`), a timestamp (in various formats), and location coordinates in the format `Loc: (X, Y)`. You need to extract the Sensor ID, Timestamp, X coordinate, and Y coordinate.
2. **Timestamp Alignment**: The extracted timestamps come in different formats (e.g., "Jan 05 2024 14:30:00", "2024/01/05 2:35 PM"). You must normalize all valid timestamps to the ISO 8601 format: `YYYY-MM-DDTHH:MM:SS` (e.g., `2024-01-05T14:30:00`). Note: You can assume the local timezone for parsing.
3. **Distance Computation**: The base station is at coordinates (0, 0). For each valid sensor, compute the Manhattan distance from the base station to the sensor's coordinates. The formula for Manhattan distance is `|X| + |Y|` (absolute value of X plus absolute value of Y).
4. **Validation Checkpoints**: 
   - A line must be completely ignored (dropped) if it does not contain a recognizable `Sensor-XX` ID.
   - A line must be dropped if the coordinates are not valid integers (e.g., `Loc: (invalid, 9)` or missing coordinates).
   - A line must be dropped if the timestamp cannot be parsed by the standard `date` command.
5. **Output**: Write the cleaned data to `/home/user/clean_sensors.csv`. The output file must have the following exact CSV header:
   `SensorID,Timestamp,X,Y,Distance`
   Following the header, output the cleaned data rows, sorted chronologically by the normalized timestamp.

Ensure your script `/home/user/clean_data.sh` has executable permissions and correctly processes the data when run without arguments. Do not hardcode the output for the specific lines; your script should use `awk`, `sed`, `grep`, `date`, or standard Bash tools to process the file generically.