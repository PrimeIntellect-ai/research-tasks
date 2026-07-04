You are a log analyst investigating patterns in a distributed sensor network. The raw telemetry logs are stored on an internal logging server that streams irregular, noisy data. 

Your objective is to build a multi-stage data processing pipeline in C++ and bash to fetch, clean, resample, and normalize this data.

**Step 1: Start the Log Server**
There is a pre-existing Python script at `/home/user/log_server.py`. Execute this script in the background to start the local log server. It will serve the raw data at `http://localhost:8123/raw_logs.csv`.

**Step 2: Develop the C++ Processor**
Write a C++ program at `/home/user/process_logs.cpp` that performs the following mathematical data processing tasks:
1. **Constraint-based validation**: Read the downloaded CSV data (which has two columns: `timestamp` and `value`). Drop any rows where `value < 0` (these represent sensor errors).
2. **Resampling and gap-filling**: The remaining timestamps are irregular (e.g., 0.0, 1.2, 2.5). Resample the data to strictly integer timestamps from `t = 0` to `t = 5` inclusive (i.e., 0, 1, 2, 3, 4, 5). Use linear interpolation between the nearest surrounding valid points to calculate the value at each integer timestamp.
3. **Normalization**: Calculate the mean and the population standard deviation of the 6 newly resampled values. Apply Z-score standardization `(value - mean) / std_dev` to each resampled value.

**Step 3: Pipeline Orchestration**
Write a bash script at `/home/user/pipeline.sh` that:
1. Compiles `/home/user/process_logs.cpp` using `g++` into an executable `/home/user/processor`.
2. Downloads the raw logs from the local server using `curl`.
3. Passes the downloaded data into your C++ processor.
4. Saves the final standardized output to `/home/user/processed_logs.csv`.

**Output Format Requirements**
The final `/home/user/processed_logs.csv` must contain exactly 6 lines (one for each integer timestamp from 0 to 5).
Each line must be in the format: `timestamp,normalized_value`
Round the `normalized_value` to exactly 4 decimal places.

Execute your pipeline to generate the final output.