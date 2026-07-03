You are a performance engineer profiling a new distributed computing application. You have collected a set of benchmark runs under varying input sizes and concurrency levels, but the application occasionally experiences network timeouts (recorded as 'Timeout' instead of 'Success'). 

You need to fit a non-linear performance model to the successful runs to understand the scaling characteristics and then find the optimal concurrency level for a target workload.

The raw profiling data is located at `/home/user/profiling_data.csv`. It contains the following columns:
- `N`: Input size (integer)
- `C`: Concurrency level (integer)
- `Time`: Execution time in seconds (float)
- `Status`: Run status (string, either 'Success' or 'Timeout')

**Step 1: Data Cleaning**
Filter the dataset to include only rows where `Status` is exactly 'Success'. Discard the rest.

**Step 2: Non-linear Model Fitting**
Fit the following non-linear execution time model to the cleaned dataset:
$$T(N, C) = a \cdot \frac{N}{C} + b \cdot C^c$$
Where:
- $T$ is the execution time.
- $N$ is the input size.
- $C$ is the concurrency level.
- $a, b, c$ are the unknown parameters to be fitted.

Find the parameters $a, b$, and $c$ that minimize the Mean Squared Error (MSE) between the model's predicted time and the actual `Time` in the cleaned dataset. 
- Use an initial guess of $a=1.0, b=1.0, c=1.0$.
- Constrain all parameters $a, b, c$ to be within the bounds $[0.1, 5.0]$.

**Step 3: Optimization**
Using the fitted parameters $a, b, c$, determine the optimal continuous concurrency level $C$ that minimizes the execution time $T$ for a target input size of $N = 50000$.
- The concurrency level $C$ must be bounded such that $C \ge 1.0$.

**Step 4: Output Verification**
Create a JSON file at `/home/user/model_results.json` containing the fitted parameters and the optimal $C$. The keys must be exactly `"a"`, `"b"`, `"c"`, and `"optimal_C"`. Round all values to exactly 4 decimal places.

Example output format:
```json
{
  "a": 1.2345,
  "b": 2.3456,
  "c": 3.4567,
  "optimal_C": 12.3456
}
```