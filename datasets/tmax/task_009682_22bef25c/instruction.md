You are assisting a machine learning researcher who is organizing datasets for an inference benchmarking suite. 

The researcher has written a C++ program (`/home/user/process.cpp`) that reads a dataset (`/home/user/dataset.csv`), normalizes a specific feature, and splits the data into a training set (first 800 rows) and a test set (remaining 200 rows).

However, the researcher accidentally introduced a **data leak**. The program currently calculates the mean and standard deviation over the *entire* dataset (all 1000 rows) before normalizing. This allows information from the test set to leak into the training set.

Your tasks are:

1. **Fix the Data Leak**: Modify `/home/user/process.cpp` so that the mean and population standard deviation are calculated **exclusively** on the training split (the first 800 rows). The test set (rows 801-1000) must then be normalized using the mean and standard deviation derived from the training set. 

2. **Compile and Run**:
   - Ensure you have the necessary C++ build tools installed (`g++`).
   - Compile the fixed `/home/user/process.cpp` into an executable named `/home/user/process_data`.
   - Run the executable. It should generate two files: `/home/user/train.csv` and `/home/user/test.csv`, each containing the headers `id,normalized_value`.

3. **Inference Benchmarking**:
   - Write a bash script at `/home/user/benchmark.sh` that executes `./process_data` exactly 5 times in a loop.
   - The script should append the string "Run complete" to `/home/user/benchmark_log.txt` after each execution.
   - Make sure `/home/user/benchmark.sh` is executable and run it once.

Ensure all file paths are exact and located in `/home/user/`.