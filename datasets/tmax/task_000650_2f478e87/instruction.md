You are a data analyst and performance engineer. We have a legacy proprietary scoring model compiled as a stripped executable located at `/app/legacy_scorer`. This binary is used to process CSV files, but it is too slow for our new inference pipeline. 

Your goal is to perfectly reimplement its mathematical logic in Rust to maximize inference performance.

Here is what we know about the legacy model:
1. It reads a single line from standard input containing exactly 4 comma-separated floating-point numbers (e.g., `1.5,2.0,-3.1,4.0`).
2. It prints a single floating-point score to standard output, formatted to 4 decimal places.
3. The underlying algorithm is a mathematical formula. Our original documentation hints that it is a polynomial equation with a maximum degree of 2.

Your tasks:
1. **Model Evaluation & Formula Extraction:** You must determine the exact mathematical formula used by `/app/legacy_scorer`. You can do this by generating synthetic CSV inputs, querying the legacy binary, and using statistical modeling/regression techniques to fit and perfectly recover the coefficients.
2. **Rust Implementation:** Create a new Rust project at `/home/user/new_scorer`. Write a Rust program that exactly duplicates the recovered mathematical logic. It must accept a 4-column CSV row on `stdin` and print the resulting score to `stdout` with 4 decimal places.
3. **Inference Optimization:** Configure the numerical and build settings in your `Cargo.toml` to optimize for inference performance (e.g., enable release mode optimizations). 
4. Compile your final binary.

The automated verification system will fuzz your compiled release binary against the legacy binary using thousands of randomly generated inputs to ensure bit-exact equivalence. Ensure your compiled binary is located at `/home/user/new_scorer/target/release/new_scorer`.