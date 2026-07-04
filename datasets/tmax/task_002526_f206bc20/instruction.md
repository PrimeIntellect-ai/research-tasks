You are an MLOps engineer tasked with building a high-performance validation utility in C. We generate massive binary files containing millions of floating-point predictions from our models, and we need a lightweight, extremely fast tool to compute numerical accuracy metrics and benchmark the evaluation time itself. This tool will append results to a continuously growing binary metrics log.

Your objective is to write, compile, and execute a C program that performs this evaluation.

Here is the specification for the C program:
1. **Source File**: Write the C code to `/home/user/mlops_eval.c`.
2. **Arguments**: The program must accept exactly three command-line arguments:
   `./mlops_eval <inference_file.bin> <truth_file.bin> <metrics_log.bin>`
3. **Data Handling (Large-scale storage)**: 
   - Both `<inference_file.bin>` and `<truth_file.bin>` contain exactly 2,500,000 IEEE 754 32-bit floats.
   - You MUST use `mmap` (read-only) to map these files into memory for maximum throughput. Do not use `fread`.
4. **Benchmarking & Accuracy Testing**:
   - Immediately before looping over the data, record the start time using `clock_gettime` with `CLOCK_MONOTONIC`.
   - Iterate through the mapped arrays and compute two metrics:
     - **MAE (Mean Absolute Error)**: The average of the absolute differences between the inference floats and the truth floats.
     - **MaxAE (Maximum Absolute Error)**: The maximum absolute difference found between corresponding floats.
   - Immediately after the loop, record the end time.
   - Calculate the elapsed computation time in **microseconds** (`uint64_t`).
5. **Logging**:
   - Open `<metrics_log.bin>` in append mode (creating it if it doesn't exist).
   - Append a tightly packed **24-byte binary record** containing:
     1. `timestamp` (uint64_t): Current UNIX time in seconds (e.g., from `time(NULL)`).
     2. `mae` (float): The calculated Mean Absolute Error.
     3. `max_ae` (float): The calculated Maximum Absolute Error.
     4. `compute_time_us` (uint64_t): The elapsed time in microseconds.
6. **Console Output**: 
   - Print the results to standard output exactly like this (with 6 decimal places):
     `MAE: [mae], MaxAE: [max_ae]`

**Task Execution Steps**:
1. Two files have already been prepared for you: 
   - `/home/user/artifacts/inference.bin`
   - `/home/user/artifacts/truth.bin`
2. Write the C code fulfilling the specifications above.
3. Compile it: `gcc -O3 -Wall mlops_eval.c -o mlops_eval -lm`
4. Run your utility: `./mlops_eval /home/user/artifacts/inference.bin /home/user/artifacts/truth.bin /home/user/metrics.log`

Ensure your C code properly handles file opening, mapping, unmapping, and closing to prevent memory/file-descriptor leaks.