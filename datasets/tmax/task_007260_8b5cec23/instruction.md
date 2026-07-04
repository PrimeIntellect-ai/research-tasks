You are tasked with building a testing and performance benchmarking harness for a custom C-based dataset cleaning library. 

In machine learning pipelines, a common critical error is "data leakage" where statistics from previous batches (like the training set) inadvertently affect the processing of subsequent batches (like the test set). 

We have a library located in `/home/user/cleaner.c` with its header `/home/user/cleaner.h`. It contains two functions for zero-centering a batch of data:
1. `void clean_batch_isolated(float* data, int size);` - Computes the mean of the current batch and subtracts it.
2. `void clean_batch_leaky(float* data, int size);` - Has a bug where it continuously aggregates sums across all batches it processes, causing a data leak.

Your objective is to set up the analysis environment, write a testing program in **C** (`/home/user/test_bench.c`), and generate a statistical report of their performance and correctness.

Here are your specific requirements:
1. **Environment**: Ensure `gcc` and standard math libraries are available.
2. **Test Data Generation**: In `test_bench.c`, initialize the random number generator with `srand(42)`. Generate a master sequence of random floats (between 0.0 and 100.0) using `(float)rand()/(float)(RAND_MAX/100)`. 
3. **Benchmarking**: 
   - You will simulate processing 100 consecutive batches of data. Each batch contains 10,000 floats.
   - For `clean_batch_isolated`, allocate a fresh array of 10,000 floats for each of the 100 batches, populate it sequentially from your random generation logic (re-seed `srand(42)` right before starting the 100 batches for the isolated test), and measure the execution time of `clean_batch_isolated` for *each* batch using `clock_gettime(CLOCK_MONOTONIC, ...)`.
   - Repeat the exact same process (re-seeding with `srand(42)` right before starting) for `clean_batch_leaky`.
4. **Statistical Analysis**:
   - Compute the mean processing time (in microseconds) across the 100 batches for both functions.
   - Compute the 95% Confidence Interval for the mean processing time for both functions. Use the formula: `CI = mean ± (1.96 * (std_dev / sqrt(n)))`.
   - Calculate the arithmetic mean of the *cleaned data values* in the **2nd batch** (Batch Index 1) for both functions.
5. **Reporting**:
   Write the results to `/home/user/report.txt` using exactly the following format (round all floats to 2 decimal places):
   ```
   Isolated Mean Time: [X.XX] us
   Isolated Time 95% CI: [[LOWER.XX], [UPPER.XX]]
   Isolated Batch 2 Data Mean: [X.XX]
   Leaky Mean Time: [X.XX] us
   Leaky Time 95% CI: [[LOWER.XX], [UPPER.XX]]
   Leaky Batch 2 Data Mean: [X.XX]
   ```

Write, compile, and run your benchmark. Save the final report exactly as specified.