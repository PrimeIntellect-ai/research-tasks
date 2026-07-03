As a Machine Learning Engineer, you are preparing a pipeline to extract statistical features from a large dataset for training. You are concerned about numerical stability issues (catastrophic cancellation) when calculating the sample variance of features that have very large means but small variances. 

To ensure the integrity of your training data, you need to evaluate a naive variance calculation against a numerically stable approach (Welford's online algorithm) and verify your Go implementation against a trusted C reference.

Please complete the following steps:

1. **Compile Reference Software**:
   You have been provided with the source code for a C-based reference implementation of Welford's algorithm at `/home/user/src/welford_ref.c`. 
   Compile this file using `gcc` and output the executable to `/home/user/bin/welford_ref`. (Create the `bin` directory if it does not exist).

2. **Generate Reference Output**:
   The training dataset is located at `/home/user/data/input.csv`. It contains a single column of floating-point numbers.
   Run the compiled `welford_ref` tool. It takes the file path as its first argument and prints the mean and sample variance. Save its exact standard output to `/home/user/output/ref_output.txt`. (Create the `output` directory if it does not exist).

3. **Implement Statistics in Go**:
   Write a Go program at `/home/user/src/stats.go` that reads `/home/user/data/input.csv` and calculates the sample variance using two different `float64` methods:
   
   *Method A (Naive)*:
   Calculate using the standard naive formula: `Sample Variance = (Sum of Squares - (Square of Sum)/n) / (n - 1)`. 
   Accumulate the sum and sum of squares in `float64` variables.
   
   *Method B (Welford's Algorithm)*:
   Implement Welford's online algorithm for sample variance in `float64`.
   For each new value `x`:
   `count += 1`
   `delta = x - mean`
   `mean += delta / count`
   `M2 += delta * (x - mean)`
   After all elements, `Sample Variance = M2 / (count - 1)`

4. **Compare and Output Results**:
   Your Go program must output a JSON file to `/home/user/output/results.json` containing the results of your calculations. The JSON must exactly match this structure:
   ```json
   {
     "naive_variance": 0.0,
     "welford_variance": 0.0,
     "welford_mean": 0.0
   }
   ```
   (Replace `0.0` with the actual computed `float64` values).

The task will be evaluated by verifying your compiled C binary, the `ref_output.txt` file, and the values in your `results.json`. The `welford_variance` should closely match the reference output, while `naive_variance` will demonstrate numerical instability.