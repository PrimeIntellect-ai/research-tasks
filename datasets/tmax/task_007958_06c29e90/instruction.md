You are an MLOps engineer tasked with reconstructing a legacy mathematical inference pipeline in C++ and benchmarking its performance. The previous Python-based pipeline had a silent bug where missing integer values in a CSV caused the entire column to be cast to floats, leading to subtle precision errors in the downstream matrix operations. 

You need to write a C++ program that strictly enforces the data schema, performs the mathematical inference using the Eigen library, and benchmarks the execution.

**Step 1: Environment Setup**
You will need `Eigen3` for matrix operations. Please download or install it and configure your build system (e.g., CMake) to use it.

**Step 2: Data Schema Enforcement**
Read the experiment artifacts from `/home/user/data/artifacts.csv`. 
The CSV has no header. The columns represent: `id, count, f1, f2, f3`.
Apply the following strict schema rules:
1. `id` (Column 0): Must be a valid integer. If it is "NaN", empty, or cannot be parsed as an integer, drop the entire row.
2. `count` (Column 1): Must be an integer. If it is empty or "NaN", impute it with `0`. If it contains a decimal point (e.g., "5.0"), drop the row to prevent silent type corruption.
3. `f1, f2, f3` (Columns 2, 3, 4): Must be floats. If any are empty or "NaN", impute the missing value with `0.0` (for simplicity in this pipeline).

**Step 3: Model Architecture Reconstruction**
After filtering and imputing, extract the `count, f1, f2, f3` columns into an $N \times 4$ Eigen matrix $X$, where $N$ is the number of valid rows.
Read the model weights from `/home/user/data/weights.txt`. It contains a single line with 4 comma-separated floats representing a $4 \times 1$ weight vector $W$.
Compute the inference result: $Y = X \times W$.
Calculate the sum of all elements in the resulting vector $Y$.

**Step 4: Inference Performance Benchmarking**
Run the matrix multiplication ($Y = X \times W$) 10,000 times in a loop. Measure the total time taken for these 10,000 iterations in milliseconds.

**Step 5: Output Generation**
Output the results to a JSON file at `/home/user/results.json` with the following exact format:
```json
{
  "valid_rows": <integer>,
  "inference_sum": <float, rounded to 4 decimal places>,
  "benchmark_time_ms": <float>
}
```

Write, compile, and execute your C++ code to generate the final JSON file. Ensure your code is robust against the corrupted data.