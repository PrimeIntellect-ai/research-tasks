You are a data engineer tasked with building a robust, numerically stable ETL pipeline to process high-frequency sensor data. The raw data contains occasional transmission errors and features values with a very large baseline but tiny fluctuations. Using a naive variance formula on this data will result in catastrophic cancellation and incorrect results.

Your objective is to build a two-stage ETL pipeline in `/home/user/`:
1. A data cleaning step using standard Bash tools.
2. A numerical aggregation step using a custom C++ program you must write.

**Step 1: The Raw Data**
A raw dataset will be located at `/home/user/raw_sensors.csv`. It has a header `timestamp,sensor_id,value`.
Some rows are corrupted (e.g., missing values, or the `value` column contains strings like "ERR" or "NaN"). 

**Step 2: C++ Aggregation Program**
Write a C++17 program named `/home/user/aggregate.cpp`. It must:
- Read CSV-formatted data from standard input (`stdin`) without a header.
- Aggregate the data by `sensor_id`.
- Compute the exact sample mean and **sample variance** (using $n-1$) for the `value` column for each `sensor_id`.
- **Crucial:** You must implement a numerically stable algorithm (like Welford's online algorithm) to compute the variance. The values are in the millions, but the differences are in the fractions. Naive $E[X^2] - E[X]^2$ will fail accuracy tests. Use `double` precision.
- Output the results to standard output (`stdout`) in the format: `sensor_id,mean,variance`.
- The floating-point numbers in the output must be formatted to exactly 6 decimal places.
- Sort the output alphabetically by `sensor_id`.

**Step 3: The ETL Pipeline Script**
Write a Bash script at `/home/user/pipeline.sh` that orchestrates the workflow. The script must:
1. Compile the C++ program using `g++ -std=c++17 -O3 aggregate.cpp -o aggregate`.
2. Parse `/home/user/raw_sensors.csv`, strip the header, and filter out any rows where the `value` column is not a valid numerical float (e.g., remove rows with "ERR", "NaN", or empty values). You must use standard shell tools (like `awk`, `sed`, or `grep`) for this cleaning step.
3. Pipe the cleaned data directly into the compiled `./aggregate` executable.
4. Redirect the final output of the C++ program to `/home/user/summary.csv`.

**Constraints:**
- Do not use any external C++ libraries besides the standard library.
- Make sure `pipeline.sh` is executable and runs successfully without user interaction.
- The final output in `/home/user/summary.csv` should not have a header line.

To complete this task, write the source code, build the script, and execute `/home/user/pipeline.sh` so that `/home/user/summary.csv` is generated with the correct values.