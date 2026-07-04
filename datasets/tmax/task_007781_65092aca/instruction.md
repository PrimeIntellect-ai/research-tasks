You are a data scientist cleaning up a messy dataset of IoT sensor readings. The data pipeline is broken, and you need to build a multi-stage pipeline using shell scripting and C to extract, normalize, and interpolate the data.

You have been provided with a messy log file at `/home/user/raw_sensor.log`. It contains mixed log messages, but you only care about the lines containing JSON payloads with temperature data.

The log lines look like this:
`[INFO] 2023-10-01T12:00:02Z - System boot`
`[DATA] 2023-10-01T12:00:15Z - payload: {"sensor_id": "T1", "temp": 23.0}`
`[WARN] 2023-10-01T12:00:18Z - Voltage drop`

Your task is to create an end-to-end pipeline:

1. **Regex Extraction (Shell):**
   Write a shell script at `/home/user/pipeline.sh` that extracts the timestamp and temperature (`temp`) from the `[DATA]` lines in `/home/user/raw_sensor.log`. You must convert the ISO8601 timestamps to standard Unix epoch seconds.

2. **Resampling and Interpolation (C Program):**
   Write a C program at `/home/user/interpolate.c`. 
   - It should read the extracted Unix timestamps and temperature values (you can pipe them in or read from a temporary file).
   - The data is irregularly spaced. You must resample the data to a fixed interval of **10 seconds**, starting from the epoch time `1696161610` (which corresponds to 2023-10-01T12:00:10Z) and ending at `1696161640`.
   - Use **linear interpolation** to calculate the temperature at exactly these 10-second intervals (i.e., calculate values for `1696161610`, `1696161620`, `1696161630`, `1696161640`). 
   - Output the result to a CSV file at `/home/user/clean_resampled.csv` with the format `timestamp,temperature` (temperature formatted to 2 decimal places).

3. **Orchestration:**
   The script `/home/user/pipeline.sh` must compile the C program (using `gcc`), perform the regex extraction, run the C program with the extracted data, and ensure `/home/user/clean_resampled.csv` is generated successfully.

**Important Constraints:**
- Use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.).
- Ensure your linear interpolation handles the floating-point math correctly: $y = y_1 + (x - x_1) \frac{y_2 - y_1}{x_2 - x_1}$.
- Do not use any external dependencies outside of standard GNU/Linux tools (`awk`, `sed`, `grep`, `date`, `gcc`).
- Run your pipeline so the final CSV is produced.