You are an automation specialist tasked with creating a data pipeline script in Go.

Your goal is to process a binary file containing encoded numerical data, compute rolling statistics, log the pipeline execution, and prepare a cron schedule for the task. 

Here are the exact requirements:

1. **Read and Decode Data**: 
   An input file is located at `/home/user/input_data.bin`. It contains a single line of comma-separated integers, but it is encoded in **UTF-16LE** (Little Endian) without a BOM. 
   Write a Go program at `/home/user/rolling_stats.go` that reads this file and decodes the characters back to standard UTF-8/strings so you can parse the integers. You may use standard library packages like `unicode/utf16` and `encoding/binary`.

2. **Compute Rolling Statistics**:
   Calculate the rolling moving average of the integers with a **window size of 3**. 
   For example, if the sequence is 2, 4, 6, 8, the rolling averages would be 4.00, 6.00.
   Output the resulting averages to `/home/user/stats.log` on a single line, separated by commas, formatted to exactly two decimal places (e.g., `4.00,6.00`).

3. **Pipeline Logging**:
   Your Go program must append a log entry to `/home/user/pipeline.log` upon successful completion. The log entry must exactly match this format:
   `SUCCESS: Processed <N> records`
   where `<N>` is the total number of integers read from the input file.

4. **Pipeline Scheduling**:
   Create a cron job definition file at `/home/user/stats_cron`. The file should contain a single line with a valid cron expression that schedules `/home/user/rolling_stats.go` to be run using `go run` every **5 minutes**. (Assume the cron daemon would execute it as the `user` user).

5. **Execution**:
   Once you have written the code, run it once manually to ensure `/home/user/stats.log` and `/home/user/pipeline.log` are generated correctly.