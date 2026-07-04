You are a bioinformatics analyst working on a Go-based tool that estimates a sequence scaling parameter using gradient descent. The tool reads a set of DNA sequences, computes their AT/GC ratios, and attempts to find a scaling factor `k` that minimizes the Mean Squared Error (MSE) between the scaled ratios and a set of target experimental values.

The project is located at `/home/user/seq_analyzer`. 

Currently, there are two issues:
1. The gradient descent implementation in `/home/user/seq_analyzer/optimize.go` has a mathematical bug in its gradient calculation for the MSE loss function. The loss function being minimized should be the standard Mean Squared Error: `MSE = (1/N) * sum((k * ratio_i - target_i)^2)`.
2. There are no regression tests to ensure the optimizer works correctly.

Your tasks are:
1. Fix the bug in `/home/user/seq_analyzer/optimize.go` so that it correctly computes the gradient of the MSE and updates `k` appropriately. 
2. Write a regression test in `/home/user/seq_analyzer/optimize_test.go` containing at least one test case: `ratios = []float64{1.0, 2.0}`, `targets = []float64{2.0, 4.0}`, `lr = 0.1`, `epochs = 100`. The test must assert that the optimized `k` is close to `2.0` (within a `0.01` tolerance). The test should pass when `go test` is run.
3. Build the Go project and run it. The program is already set up to read `/home/user/data/sequences.txt` and `/home/user/data/targets.txt`, but it outputs to stdout. Modify `main.go` or redirect its output so that the final optimized `k` (formatted to exactly 4 decimal places) is written to `/home/user/result.txt`.

Ensure your test passes and `/home/user/result.txt` contains only the optimized `k` value.