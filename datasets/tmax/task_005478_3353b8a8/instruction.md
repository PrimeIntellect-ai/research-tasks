You have inherited a legacy data processing pipeline written in Go, located at `/home/user/data_processor`. 

The program, `main.go`, reads a CSV file containing a single column of floating-point sensor readings and calculates the population standard deviation of the entire dataset. However, there is a subtle bug: when running the program on the provided production dataset (`/home/user/data_processor/dataset.csv`), the program outputs `NaN` (Not a Number) instead of the correct standard deviation.

Your objective is to diagnose and fix this issue using test minimization and precision debugging:

1. **Delta Debugging / Test Minimization:**
   The `NaN` output is triggered by a precision loss issue that accumulates as more rows are processed. Find the **exact minimum number of rows** (reading from the beginning of `dataset.csv`) that causes the program to output `NaN`. 
   Write this integer (the 1-indexed row count) to `/home/user/data_processor/failing_row.txt`.

2. **Fix the Precision Loss:**
   Modify `/home/user/data_processor/main.go` to eliminate the precision loss. The underlying algorithm suffers from catastrophic cancellation because it uses `float32` for intermediate state tracing and accumulation.
   * Do not change the final `fmt.Printf("%.6f\n", ...)` output format.
   * You may upgrade types to `float64` or rewrite the variance calculation to be numerically stable.

3. **Produce the Final Output:**
   Compile your fixed program and run it on the full `dataset.csv`.
   Save the standard output of your fixed program to `/home/user/data_processor/final_result.txt`.

**Constraints:**
- Your final executable must be compiled to `/home/user/data_processor/processor` using `go build -o processor main.go`.
- Only use standard Bash utilities and the Go toolchain.