You are a Machine Learning Engineer preparing a mathematical training dataset for a new neural-symbolic model. You need to process a large text file containing mathematical expressions, simulate inference evaluation at different numerical precisions, and track the numerical accuracy and parsing performance.

Your task is to create a Rust application that processes this dataset.

Here are the requirements:
1. Initialize a new Rust project named `math_prep` in `/home/user/math_prep`.
2. The input dataset will be located at `/home/user/dataset.txt`. It contains 10,000 lines. Each line contains a simple mathematical expression in the exact format: `[FLOAT] [OP1] [FLOAT] [OP2] [FLOAT]`
   - `[FLOAT]` are standard floating-point numbers.
   - `[OP1]` and `[OP2]` are operators, restricted to either `+` or `*`.
   - Components are separated by a single space.
3. Your Rust program must read this file and evaluate every expression twice to test numerical accuracy:
   - **f32 Evaluation**: Parse the strings directly into `f32`, and perform the math using `f32` variables.
   - **f64 Evaluation**: Parse the strings directly into `f64`, and perform the math using `f64` variables.
   *Note: Standard mathematical precedence applies (multiplication `*` must be evaluated before addition `+`).*
4. Calculate the Mean Squared Error (MSE) between the `f32` evaluations and `f64` evaluations across all 10,000 lines. The `f64` result should be treated as the ground truth. Cast `f32` results to `f64` before computing the squared difference.
5. Benchmark the time taken to perform the reading, parsing, and dual-evaluation of the entire file. Record the duration in milliseconds.
6. Write the results to an experiment tracking CSV file at `/home/user/experiment_log.csv`. The file must have exactly the following header and one row of data:
   `num_samples,mse,duration_ms`
   - `num_samples`: The total number of expressions evaluated (should be 10000).
   - `mse`: The computed Mean Squared Error, formatted to 6 decimal places.
   - `duration_ms`: The total time taken in integer milliseconds.

Ensure your program compiles and runs successfully, outputting the correct CSV file. Do not use external crates for mathematical evaluation; implement the simple parsing and standard precedence logic yourself using standard Rust. You may use `cargo run --release` to execute your program.