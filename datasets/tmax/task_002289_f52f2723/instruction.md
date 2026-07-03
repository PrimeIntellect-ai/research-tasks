You are assisting a researcher organizing datasets who needs to evaluate the performance of a lightweight mathematical model on bootstrapped subsamples of a dataset. 

The researcher has a dataset located at `/home/user/dataset.csv`. The file has a header and two columns: `x` and `true_y`. 

Your task is to write a reproducible C++ pipeline that performs bootstrap sampling, runs inference, validates the outputs by computing the Mean Squared Error (MSE), and benchmarks the inference time.

Please write a C++ program at `/home/user/evaluator.cpp` that does the following:
1. Takes 5 command-line arguments: `<input_csv> <num_iterations> <sample_size> <seed> <output_txt>`
2. Reads the CSV data into memory (ignoring the header). Let $N$ be the number of rows.
3. Performs `<num_iterations>` iterations of bootstrap sampling. In each iteration:
   - Draws `<sample_size>` samples (rows) with replacement.
   - **Crucial Reproducibility Requirement**: Because standard library RNGs vary across compilers, use this exact Linear Congruential Generator (LCG) logic to pick row indices (0-indexed):
     - Initialize `uint64_t state = seed;` BEFORE the loop over iterations.
     - To pick each sample's index:
       `state = (1103515245 * state + 12345) % 2147483648;`
       `int row_index = state % N;`
   - **Benchmarking**: Record the time taken ONLY for the inference step. Use `std::chrono::high_resolution_clock`.
   - **Inference**: For each drawn row, compute the predicted value using the regression model: $f(x) = 2.5 + 1.2x - 0.3x^2$
   - Stop the timer after computing all predictions for the sample.
   - **Validation**: Compute the Mean Squared Error (MSE) between the predicted values and the drawn `true_y` values for this sample.
4. Calculates the average MSE across all iterations, and the average inference time (in microseconds) across all iterations.
5. Writes the final results to `<output_txt>` in the exact following format:
   ```
   Avg_MSE: <value>
   Avg_Time_us: <value>
   ```
   Format the `Avg_MSE` to exactly 4 decimal places.

After writing the code, compile it using `g++ -O3 -std=c++17 -o /home/user/evaluator /home/user/evaluator.cpp`.
Then, run it with the following arguments:
- Input: `/home/user/dataset.csv`
- Iterations: `1000`
- Sample Size: `50`
- Seed: `42`
- Output: `/home/user/results.txt`