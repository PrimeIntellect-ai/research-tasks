You are an operations engineer triaging an urgent incident. The finance team reported that the `fin-aggregator` data pipeline has started producing inaccurate daily totals. The output is experiencing severe numerical instability, leading to discrepancies of thousands of dollars on large datasets. 

The source code repository is located at `/home/user/fin-aggregator`. The pipeline transforms JSON records into an aggregated sum. 

Your tasks are to:
1. Use `git bisect` to identify the exact commit that introduced the regression. The repository has a test suite (`go test`) that fails on the bad commit. The first commit in the repository is known to be good.
2. Diagnose the root cause of the numerical instability. You may need to use an interactive debugger (`dlv`) or insert assertion-based intermediate validations to see where the data transformation diff diverges.
3. Fix the bug in the Go code so that `go test` passes and the numerical instability is resolved.
4. Process the provided production dataset (`data/input.json`) using the fixed program: `go run main.go data/input.json`.

Finally, create a report file at `/home/user/resolution.txt` containing exactly two lines:
- Line 1: The full Git commit hash of the bad commit that introduced the bug.
- Line 2: The correct numerical output (a single floating-point number formatted to two decimal places) of the `fin-aggregator` when processing `data/input.json`.

Ensure you do not alter the Git history or create new commits. Just fix the working tree and run the program.