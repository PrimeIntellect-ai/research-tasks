You are acting as a data engineer for a data scientist who needs a continuous cleaning and anomaly detection pipeline for 2D sensor data. The data arrives as CSV files. 

Your objective is to create a C program to process this data, a Bash script to orchestrate the pipeline, and a cron job schedule to automate it.

**Phase 1: Environment Setup**
Create the following directory structure:
- `/home/user/pipeline/input/` (where new CSVs will arrive)
- `/home/user/pipeline/output/` (where the C program will write results)
- `/home/user/pipeline/archive/` (where processed CSVs will be moved)
- `/home/user/pipeline/bin/` (where your executable and scripts will reside)

**Phase 2: The C Data Processor**
Write a C program at `/home/user/pipeline/bin/detector.c` and compile it to `/home/user/pipeline/bin/detector`. You must link the math library (`-lm`).
The program should take exactly two command-line arguments: the input CSV file path and the output file path.

*Input CSV Format:* No header. Each line has three comma-separated values: `timestamp` (integer), `sensor_x` (double), `sensor_y` (double).
*Algorithm:*
1. Calculate the Euclidean distance between the `(sensor_x, sensor_y)` coordinates of the *current* row and the *previous* row. (The first row has no previous row, so no distance is calculated and it is never an anomaly).
2. If the Euclidean distance is strictly greater than `50.0`, the current row is flagged as a "changepoint anomaly".
3. Calculate the overall mean of `sensor_x` and `sensor_y` across all rows in the file.

*Output Format:*
Write the following exactly to the output file path:
```
Mean X: <mean_x formatted to 2 decimal places>
Mean Y: <mean_y formatted to 2 decimal places>
Anomaly Count: <integer count of anomalies>
Anomaly Timestamps: <comma-separated list of anomaly timestamps, or "None" if 0>
```

**Phase 3: The Pipeline Wrapper**
Write a Bash script at `/home/user/pipeline/bin/process.sh` that:
1. Loops over any `.csv` files in `/home/user/pipeline/input/`.
2. For each file (e.g., `data1.csv`), runs the `detector` program to produce an output file in the output directory with a `.out` extension (e.g., `/home/user/pipeline/output/data1.out`).
3. Moves the processed `.csv` file to `/home/user/pipeline/archive/`.
Make sure `process.sh` is executable.

**Phase 4: Scheduling**
Create a crontab file at `/home/user/pipeline.cron` containing a single cron expression that schedules `/home/user/pipeline/bin/process.sh` to run every 5 minutes. (Do not install it via the `crontab` command, just create the file so it can be verified).

Complete all phases and ensure your code compiles and works correctly. You may test it with dummy data.