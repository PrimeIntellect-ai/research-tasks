You are a data engineer tasked with building a lightweight ETL pipeline using only standard Linux shell tools (Bash, awk, sed, grep, etc.). 

You have been provided with a raw, unstructured log file at `/home/user/sensor_stream.log`. This file contains telemetry data from various IoT devices. Your goal is to extract specific information, validate the data against strict constraints, derive a new feature, and output the clean data as a CSV file.

### Input Format
Each line in `/home/user/sensor_stream.log` follows this general structure:
`YYYY-MM-DD HH:MM:SS | <LOG_LEVEL> | IP: <ip_address> | MSG: [key1=value1] [key2=value2] ...`

### Extraction & Validation Rules
You must process each line and extract the `timestamp`, `ip_address`, `temp`, and `humidity`. 
A line is considered **VALID** only if it meets ALL of the following criteria. If a line fails any criterion, it must be completely discarded.

1.  **IP Address**: Must be a valid IPv4 address (four integers separated by dots, where each integer is strictly between 0 and 255 inclusive).
2.  **Temperature (`temp`)**: The message block must contain a `[temp=X]` pair. `X` must be an integer, and it must be between `-50` and `150` inclusive.
3.  **Humidity (`humidity`)**: The message block must contain a `[humidity=Y]` pair. `Y` must be an integer, and it must be between `0` and `100` inclusive.

*Note: The order of the key-value pairs in the MSG block may vary, and there may be other irrelevant keys (like `status`).*

### Transformation
For all valid rows, you must compute a new feature called `risk_level`:
*   Set `risk_level` to `HIGH` if `temp` is strictly greater than `80` OR `humidity` is strictly greater than `90`.
*   Otherwise, set `risk_level` to `LOW`.

### Output Specification
Create a normalized CSV file at `/home/user/clean_sensors.csv`.
The file must include a header row exactly as follows:
`timestamp,ip,temp,humidity,risk_level`

Following the header, append the extracted and transformed data for all **VALID** rows in the exact order they appeared in the original log file.

Example of a valid output row:
`2023-10-01 10:00:00,192.168.1.10,45,60,LOW`

Write a bash script or use command-line tools to generate this exact output file.