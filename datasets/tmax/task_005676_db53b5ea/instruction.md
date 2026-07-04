You are a data scientist working on cleaning a large dataset of sensor readings. You have a C program that acts as a fast, pipeline-friendly anomaly detector using a simple probabilistic model (Gaussian distribution assumption). It filters out rows where the sensor reading's Z-score exceeds 2.5. 

However, the current C program (`/home/user/filter.c`) has a few critical bugs related to data types and math functions that cause it to incorrectly filter the data. 

Your task is to:
1. Fix the bugs in `/home/user/filter.c`. The program takes two command-line arguments: `mean` and `stddev` (both floats). It reads a CSV from `stdin`, expects the sensor reading to be in the second column (index 1, zero-based, after the first comma), and outputs the row to `stdout` if the absolute Z-score of the reading is `<= 2.5`. Note that the first row is a header and should always be passed through.
2. Compile the fixed program to `/home/user/filter` using `gcc -O3 filter.c -o filter -lm`.
3. Create a bash script `/home/user/pipeline.sh` that performs pipeline reproducibility testing and inference benchmarking. The script must:
   - Execute the compiled `filter` program on `/home/user/sensor_data.csv`, using a mean of `45.5` and a standard deviation of `3.2`.
   - Redirect the filtered output to `/home/user/cleaned.csv`.
   - Measure the execution time of this filtering step using the `/usr/bin/time -p` command. Redirect the timing output (which includes real, user, and sys times) to `/home/user/benchmark.txt` (stderr from `time` should be captured here).
   - Compute the MD5 checksum of `/home/user/cleaned.csv` using `md5sum` and save the output to `/home/user/checksum.txt`.

The dataset `/home/user/sensor_data.csv` has three columns: `id,sensor_val,timestamp`.

Ensure your bash script is executable (`chmod +x /home/user/pipeline.sh`) and run it so the final output files are generated.