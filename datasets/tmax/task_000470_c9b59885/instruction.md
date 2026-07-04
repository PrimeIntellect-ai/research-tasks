You are a data engineer building an ETL pipeline to process a batch of raw time-series telemetry from IoT sensors.

You have been provided a messy raw data file at `/home/user/raw_telemetry.txt`.
Each line in this file follows the format: `timestamp;sensor_id;temperature;notes`

Your task is to build a small pipeline (using bash commands and a custom C program) that does the following:
1. Filters the data to only include records for the sensor `SENS_88`.
2. Sorts the filtered records chronologically by `timestamp` (ascending).
3. Processes the sorted data using a C program you must write and compile.

The C program (which you should write to `/home/user/processor.c` and compile to `/home/user/processor`) must read the sorted data and:
* Tokenize each line based on the `;` delimiter.
* Calculate a rolling simple moving average of the `temperature` over a window of the last 3 readings (including the current reading). For the first reading, the average is just the first temperature. For the second, it's the average of the first two.
* Normalize the `notes` field by stripping out any characters that are NOT printable ASCII characters. Keep only characters with ASCII values from 32 to 126 (inclusive).
* Write the results to `/home/user/etl_output.csv`.

The output file `/home/user/etl_output.csv` must be a standard CSV where each line corresponds to a processed reading, in this exact format:
`timestamp,rolling_average,cleaned_notes`

Requirements:
- The `rolling_average` must be printed as a floating-point number formatted to exactly 2 decimal places.
- Your C program should be robust enough to handle the input data format.
- Do not include header lines in your output CSV.