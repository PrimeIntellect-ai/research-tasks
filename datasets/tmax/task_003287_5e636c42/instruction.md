You are an ML Engineer preparing a robust data preprocessing pipeline. You need to create a bash script `/home/user/evaluate_pipeline.sh` that implements and tests a data standardization pipeline.

First, write a Python script `/home/user/preprocess.py` that does the following:
1. Reads a CSV file named `/home/user/raw_data.csv` (which contains 3 numerical columns: `f1`, `f2`, `f3`).
2. Standardizes each column (subtracts the mean and divides by the sample standard deviation (ddof=1)).
3. Saves the resulting standardized data to `/home/user/processed_data.csv` with a header and 6 decimal places of precision.

Then, write the bash script `/home/user/evaluate_pipeline.sh` to perform the following tests:
1. **Reproducibility Test**: Run `/home/user/preprocess.py` twice. Save the output of the first run as `run1.csv` and the second as `run2.csv`. Compare the files. If they are exactly identical, write the word `REPRODUCIBLE` to `/home/user/reproducibility.log`. Otherwise, write `DIVERGENT`.
2. **Numerical Accuracy Test**: Create a Python inline script inside the bash script that reads `/home/user/processed_data.csv`, calculates the mean and standard deviation (ddof=1) of each column. If the absolute value of the mean is < 1e-5 and the standard deviation is between 0.99999 and 1.00001 for all columns, write `ACCURATE` to `/home/user/accuracy.log`. Otherwise, write `INACCURATE`.
3. **Performance Benchmark**: Use the `/usr/bin/time -p` command to benchmark the execution of `/home/user/preprocess.py`. Redirect the output of the `time` command to `/home/user/benchmark.log`.

Make sure `/home/user/evaluate_pipeline.sh` is executable. You do not need to create `/home/user/raw_data.csv`; assume it will be present when your script is tested. However, you can create a dummy one to test your scripts.

Ensure your bash script runs successfully without user interaction and generates the three log files: `reproducibility.log`, `accuracy.log`, and `benchmark.log`.