You are an automation specialist managing a workflow for processing 3D spatial sensor data. 

We receive raw telemetry data in `/home/user/raw_telemetry.csv`. The file has the following format:
`timestamp,x,y,z,status`
Where `timestamp` is a UNIX epoch integer, `x`, `y`, `z` are floating-point coordinates, and `status` is a text string. 

Because of a bug in the upstream sensor, some `status` fields contain unescaped, embedded newlines, which causes a single record to be split across multiple lines.

Your task is to build a robust pipeline to process this data.

1. Write a C program at `/home/user/aggregate.c` that does the following:
   - Reads the CSV data from standard input.
   - Silently drops any row that is broken (e.g., lines that do not contain exactly 4 commas due to embedded newlines).
   - For valid rows, extracts the mathematical feature: `magnitude = sqrt(x^2 + y^2 + z^2)`.
   - Performs time-based bucketing: groups the valid data into 1-hour buckets based on the timestamp (bucket = `timestamp / 3600`).
   - Calculates the average magnitude for each hour bucket.
   - Prints the result to standard output in CSV format: `hour_bucket,average_magnitude`. The average magnitude must be formatted to exactly 2 decimal places (e.g., `472222,9.50`). The output should be sorted by `hour_bucket` in ascending order.

2. Create a shell script at `/home/user/run_pipeline.sh` that:
   - Compiles `/home/user/aggregate.c` into an executable at `/home/user/aggregate` (using `-lm` for math).
   - Runs the executable, piping in `/home/user/raw_telemetry.csv` and saving the output to `/home/user/summary.csv`.
   - Make sure the script is executable.

3. Schedule this pipeline to run automatically. Install a cron job for the current user that executes `/home/user/run_pipeline.sh` at exactly 15 minutes past every hour.

Note: You can assume the input dataset is small enough to be fully processed in memory by your C program.