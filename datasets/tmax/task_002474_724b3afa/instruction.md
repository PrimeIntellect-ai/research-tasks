You are an AI assistant helping a data scientist clean noisy sensor time-series data. 

We have a directory `/home/user/sensor_data/` containing 4 CSV files: `data_0.csv`, `data_1.csv`, `data_2.csv`, and `data_3.csv`. Each file represents a different sensor batch and contains data in the format `timestamp,value` (where timestamp is an integer and value is a float).

Your task is to build a small data processing pipeline using C and bash:

1. Write a C program named `/home/user/smoother.c` that performs a rolling window aggregation to smooth the noise.
   - The program should take two command-line arguments: an input file path and an output file path.
   - It must read the CSV, and for each row, compute the simple moving average of the `value` column using a **window size of 3** (i.e., the current row's value and the up to 2 previous rows' values).
   - If fewer than 3 values are available (for the first two rows), average the available values.
   - The output should be written to the output file in the format `timestamp,smoothed_value`, where `smoothed_value` is formatted to exactly 2 decimal places (e.g., `%.2f`).

2. Write a bash script named `/home/user/pipeline.sh` that orchestrates this cleaning job:
   - It should compile `smoother.c` into an executable named `smoother` using `gcc`.
   - It must create an output directory `/home/user/clean_data/`.
   - It must run the `smoother` executable on all 4 CSV files in `/home/user/sensor_data/` **in parallel** as background processes, writing the outputs to `/home/user/clean_data/clean_0.csv`, `clean_1.csv`, etc.
   - It must wait for all parallel smoothing jobs to finish.
   - Finally, it must merge all the smoothed files into a single file at `/home/user/final_clean.csv`, sorting the combined results numerically by the `timestamp` column.

To complete the task, provide the C code and bash script, and ensure that running `bash /home/user/pipeline.sh` produces the correct `/home/user/final_clean.csv` output.