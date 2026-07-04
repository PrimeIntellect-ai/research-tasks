You are a DevOps engineer tasked with debugging a numerical instability issue in a production data processing pipeline. 

We have a compiled Rust binary located at `/home/user/engine` that reads a CSV file containing pairs of floating-point numbers, performs a sequence of mathematical operations, and prints the results. Recently, our logs show that occasionally the engine produces `NaN` (Not a Number) for certain inputs, breaking downstream systems.

We do not have the original Rust source code available on this server, only the compiled binary and a sample of the production inputs located at `/home/user/vectors.csv`.

Your objectives are:
1. **Delta Debugging / Minimization:** Identify the exact single line from `/home/user/vectors.csv` that evaluates to `NaN` when passed through the engine. You may run the binary with subsets of the input to isolate the issue. Save this exact single line to `/home/user/minimal_bug.csv`.
2. **Binary Reverse Engineering:** Analyze the `/home/user/engine` binary (using tools like `objdump`, `nm`, `strings`, or `gdb`) to determine which specific floating-point math function from the standard library is causing the numerical instability (i.e., the function that receives an out-of-bounds input and returns `NaN`). 
3. Write the exact name of this standard library math function (e.g., `sqrt`, `tan`, `acos`, `asin`, `log10`) to `/home/user/bug_cause.txt`.

The binary is executed as:
`/home/user/engine <path_to_csv>`

Ensure your final output files are precisely formatted:
- `/home/user/minimal_bug.csv` must contain exactly one line with the comma-separated floating-point pair.
- `/home/user/bug_cause.txt` must contain exactly one word (the math function name).