You are an assistant helping a data scientist clean and normalize mathematical sensor data. The raw data is continuously appended to `/home/user/sensor_data.log`, but it contains erratic formatting, error messages, and mixed units.

Your goal is to build an automated pipeline that extracts valid readings, normalizes them mathematically using a custom C program, generates a summary report from a template, and schedules this pipeline.

Here are your specific instructions:

1. **Write a C program (`/home/user/normalize.c`)**:
   - The program should read lines from standard input (stdin).
   - Expected input format per line (after regex extraction): `<ID> <RawValue> <Unit>`
     Example: `A1 1500 mV` or `B2 2.5 V`
   - Normalize the value to Volts (V). If the unit is `mV`, divide by 1000. If `V`, keep it as is.
   - Apply the mathematical calibration formula: $V_{calibrated} = V_{raw}^2 + 0.5 \times V_{raw}$
   - Output to standard output (stdout) in CSV format: `<ID>,<CalibratedValue>`
   - The `<CalibratedValue>` must be formatted to exactly 4 decimal places.
   - Compile it to an executable named `/home/user/normalize`.

2. **Create a processing shell script (`/home/user/process.sh`)**:
   - The script must read `/home/user/sensor_data.log`.
   - Use standard bash tools (like `grep`, `sed`, or `awk`) and regex to filter out corrupted lines (e.g., lines starting with `ERROR`) and extract just the ID, Value, and Unit. The raw log lines look like `[Timestamp] ID:<ID> VALUE:<RawValue> <Unit> <extra...>`
   - Pipe the extracted data (formatted as `<ID> <RawValue> <Unit>`) into your compiled C program (`/home/user/normalize`).
   - Save the final CSV output to `/home/user/clean_data.csv`.
   - Count the number of valid records processed and replace the string `{{COUNT}}` in the template file `/home/user/report.tmpl`. Save the resulting text to `/home/user/report.md`.

3. **Schedule the pipeline**:
   - Create a file `/home/user/cron_schedule.txt` containing the exact crontab entry (just the single line) that would schedule `/home/user/process.sh` to run every day exactly at midnight (00:00).

Make sure `/home/user/process.sh` is executable and run it once to generate the initial `clean_data.csv` and `report.md`.

*Note: The raw data file `/home/user/sensor_data.log` and template `/home/user/report.tmpl` already exist on the system.*