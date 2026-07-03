You are a data analyst tasked with processing a messy CSV extract of IoT temperature sensor data. You must perform data normalization, reshape the data from wide to long format, and compute a rolling aggregation entirely using standard Linux command-line tools (Bash, awk, sed, sort, etc.). **Do not use Python, Perl, or any other scripting languages.**

The input file is located at `/home/user/raw_sensors.csv`.

Here are the issues with the raw data:
1. The header names have inconsistent capitalization and extra spaces.
2. The data values contain random leading and trailing spaces.
3. The data is in a "wide" format, where each sensor has its own column (e.g., `Time_stamp, SENSOR_x , sensor_Y,Sensor_Z`).

You need to write a shell script or use a pipeline of command-line tools to process the file and create a new file at `/home/user/processed_sensors.csv` that meets the following precise specifications:

**1. Normalization:**
- All leading and trailing whitespace must be removed from every field.
- The header row must be completely uppercase.

**2. Reshaping (Wide to Long):**
- Transform the data from wide format to long format.
- The output CSV must have exactly four columns: `TIMESTAMP,SENSOR_NAME,TEMP,SMA_3`
- The first three columns correspond to the normalized timestamp, the normalized uppercase sensor name (e.g., `SENSOR_X`), and the temperature value.

**3. Windowed Aggregation:**
- The fourth column, `SMA_3`, must be a 3-period Simple Moving Average of the `TEMP` for that specific sensor.
- The moving average is calculated over the current row and up to 2 preceding rows for the *same* sensor, based on chronological order.
- If a sensor has fewer than 3 readings available up to that point, calculate the average of the available readings (1 or 2).
- Format the `SMA_3` values to exactly two decimal places (e.g., `45.00`, `45.50`, `49.67`).

**4. Sorting:**
- The final output file (excluding the header row) must be sorted ascending by `SENSOR_NAME`, and then ascending by `TIMESTAMP`.
- The header row `TIMESTAMP,SENSOR_NAME,TEMP,SMA_3` must be the first line of the output file.

Create the final normalized, reshaped, and aggregated file at `/home/user/processed_sensors.csv`.