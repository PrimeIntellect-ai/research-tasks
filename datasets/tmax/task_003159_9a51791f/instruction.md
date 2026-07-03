You are a data scientist tasked with fixing and automating a sensor data pipeline. 

We receive daily sensor readings in CSV format, but our current tools break because the `notes` column frequently contains embedded newline characters within quotes (e.g., `"this is a note\nwith a newline"`). 

Your objective is to build a robust C-based processing pipeline that correctly handles these embedded newlines, calculates summary statistics, detects anomalies, and runs on a daily schedule.

Here are your specific instructions:

1. **Write the C Processor:**
   Create a C program at `/home/user/pipeline/process_sensor.c`.
   The program must read a CSV file passed as the first command-line argument.
   The CSV has the following header: `id,timestamp,temp,humidity,notes`
   
   Your C program must correctly parse the CSV, treating any newline (`\n`) enclosed in double-quotes (`"`) as part of the field rather than a new record delimiter.
   
   The program must calculate:
   - The total number of valid data rows (excluding the header).
   - The average of the `temp` column (as a float).
   - The number of temperature anomalies. An anomaly is defined strictly as any `temp` strictly greater than `45.0`.

   The program must append its findings to `/home/user/pipeline/results.log` in exactly this format on a single line:
   `Records: <count>, AvgTemp: <average_rounded_to_2_decimal_places>, Anomalies: <count>`
   (e.g., `Records: 150, AvgTemp: 23.45, Anomalies: 4`)

2. **Create the Automation Script:**
   Create a bash script at `/home/user/pipeline/run_job.sh`.
   This script must:
   - Compile `/home/user/pipeline/process_sensor.c` into an executable named `process_sensor` in the same directory (using `gcc`).
   - Execute the compiled program, passing `/home/user/data/raw_sensor.csv` as the argument.
   Make sure the bash script is executable.

3. **Schedule the Pipeline:**
   Install a cron job for the current user that executes `/home/user/pipeline/run_job.sh` every day at exactly 3:15 AM.

**Environment details:**
- The input data is located at `/home/user/data/raw_sensor.csv`.
- You must create the `/home/user/pipeline` directory.
- Standard libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.) are available. 
- You may use any standard C logic to parse the file, but remember that standard `fgets` will stop at embedded newlines unless you write logic to track open/closed quote states.