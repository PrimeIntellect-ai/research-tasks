You are a data scientist working on a C-based data processing pipeline. We have a simple custom C program that normalizes tabular data (standardization: subtracting the mean and dividing by the standard population deviation) and splits it into a training and a test set.

However, a junior developer introduced a "data leakage" bug: the program calculates the mean and standard deviation using the *entire* dataset (train + test) before splitting, instead of calculating the statistics strictly on the training set and applying them to both.

Your tasks are:
1. Review the code in `/home/user/cleaner.c`. Fix the data leakage bug so that the mean and standard deviation are calculated *only* using the training portion (the first 80% of the rows, as hardcoded). These training statistics should then be used to normalize both the training and test rows.
2. Compile your corrected C code into an executable named `/home/user/cleaner`.
3. Run the executable on `/home/user/data.csv`. It should automatically generate `/home/user/train_norm.csv` and `/home/user/test_norm.csv` with the normalized values formatted to 4 decimal places.
4. To measure inference and processing performance, write a benchmark script `/home/user/benchmark.sh` that runs the `cleaner` executable 20 times. It should record the execution time of each run. Calculate the average execution time (in seconds) and write this single float value to `/home/user/benchmark_avg.txt`.

The CSV files must contain the original indices and the newly normalized values, separated by a comma. Do not change the 80/20 split logic, only the calculation of the statistical parameters.