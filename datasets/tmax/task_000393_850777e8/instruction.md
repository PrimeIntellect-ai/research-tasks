You are an ML engineer preparing a deterministic training data pipeline. You have a C++ program at `/home/user/data_gen.cpp` that performs feature extraction over a 2D mesh (a 1000x1000 grid decomposed into 10 sub-domains) and computes a global linear regression (slope and intercept) using multi-threading.

Currently, the C++ program computes thread-local sums and uses a mutex to accumulate them into global variables (`sum_x`, `sum_y`, `sum_xy`, `sum_xx`). Due to the non-associativity of floating-point addition and the random order in which threads complete and acquire the mutex, the final regression parameters vary slightly between runs. This non-reproducibility is unacceptable for the ML pipeline.

Your task:
1. Modify `/home/user/data_gen.cpp` so that the reduction of the thread-local sums into the global sums is **strictly reproducible and deterministic**. 
2. You must enforce a deterministic, sequential reduction order. Specifically, accumulate the block sums in the main thread in strict order of their `thread_id` (from `0` to `NUM_THREADS - 1`) after all threads have joined. Do not use the mutex for the accumulation of the global sums.
3. Compile your modified C++ code (e.g., `g++ -O3 -pthread /home/user/data_gen.cpp -o /home/user/data_gen`).
4. Run the program to generate the output file `/home/user/regression_result.txt`.

The output file `/home/user/regression_result.txt` must contain exactly one line with the comma-separated `slope,intercept` formatted to 9 decimal places (this format is already implemented in the provided code's output section).