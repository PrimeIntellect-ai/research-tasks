You are an Operations Engineer triaging an incident involving our Go-based telemetry processor. The processor recently crashed during a nightly batch run, and we are currently unable to process the day's metrics.

There are three parts to this incident that you must resolve:

**Phase 1: Memory Dump Analysis**
When the processor crashed, it dumped a chunk of its memory to disk at `/home/user/dump.bin`. The application was holding a temporary recovery token in memory at the time. 
Extract this token from the binary dump. The token is an ASCII string that begins exactly with `RECOVERY_TOKEN_` followed by a hexadecimal string.
Save this entire string (including the prefix) to `/home/user/token.txt`.

**Phase 2: Delta Debugging / Test Minimization**
The Go source code for the telemetry processor is located at `/home/user/app/main.go`, and the input dataset is at `/home/user/app/data.csv`.
If you run `cd /home/user/app && go run main.go data.csv`, the program panics with a convergence failure assertion. 
We need to know exactly which record in `data.csv` is causing the crash. Use delta debugging, bisection, or standard text filtering tools to isolate the single failing row.
Save the exact, unmodified line from `data.csv` that triggers the panic to `/home/user/failing_row.csv`.

**Phase 3: Floating-Point Precision & Convergence Repair**
Review the Go code in `/home/user/app/main.go`. The panic is caused by a floating-point precision bug in the `computeMetric` function (a custom iterative algorithm) which fails to converge within the allowed iterations due to type precision truncation.
Modify `main.go` to fix the floating-point precision issue so that the algorithm converges properly for all inputs in the CSV. Do not change the underlying mathematical formula or the tolerance logic, just upgrade the precision of the calculation where necessary to prevent the oscillation/truncation error.
Once fixed, compile and run the program against the full `data.csv`. The program will output a final aggregated metric.
Save the standard output of the successful run to `/home/user/result.txt`.

Ensure all requested files (`/home/user/token.txt`, `/home/user/failing_row.csv`, `/home/user/result.txt`) are created with the exact requested contents before completing your task.