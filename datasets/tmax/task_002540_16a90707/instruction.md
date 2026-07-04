You are an MLOps engineer tracking inference artifacts. We have received a new custom C kernel for linear layer inference (matrix-vector multiplication) from the optimization team. Before we deploy it, we need to benchmark its inference performance and verify its numerical accuracy against a standard reference implementation.

The optimized kernel source and header are located at:
- `/home/user/mlops/kernel.c`
- `/home/user/mlops/kernel.h`

The header defines the following function:
`void kernel_infer(const float* weights, const float* inputs, float* outputs, int n);`
(Where `weights` is an `n` x `n` matrix flattened in row-major order, `inputs` is an array of size `n`, and `outputs` is an array of size `n`).

Your task is to write a benchmarking program in C at `/home/user/mlops/evaluator.c` that performs the following steps:
1. Iterate over three hyperparameter sizes (matrix dimensions) $N \in \{100, 200, 300\}$.
2. For each $N$, dynamically allocate memory for `weights`, `inputs`, `outputs` (for the kernel), and `ref_outputs` (for your reference calculation).
3. Initialize the `weights` and `inputs` arrays with a constant value of `0.01f`. Initialize `outputs` and `ref_outputs` to `0.0f`.
4. Calculate the reference outputs using a standard $O(N^2)$ nested loop for matrix-vector multiplication: $ref\_outputs[i] = \sum_{j=0}^{N-1} weights[i \times N + j] \times inputs[j]$.
5. Call `kernel_infer` to populate `outputs`.
6. Compute the Maximum Absolute Error (MAE) between `outputs` and `ref_outputs` across all $N$ elements.
7. To benchmark performance, measure the total wall-clock time it takes to run `kernel_infer` **1,000 times** consecutively for the current $N$. Use `clock_gettime` with `CLOCK_MONOTONIC`.
8. Output the results for each $N$ as a new line in a CSV file at `/home/user/mlops/report.csv`. 

The CSV file must have exactly no header row, and contain exactly three lines formatted strictly as:
`N,MAE,Time_microseconds`
(e.g., `100,0.000000,1450.5`)
*Note: Format the MAE to 6 decimal places (e.g., `%f`), and the time in microseconds to 1 decimal place (e.g., `%.1f`).*

Compile your evaluator using `gcc` with `-O3` and the standard math library (`-lm`), link it with `kernel.c`, and execute it to generate the `report.csv`.