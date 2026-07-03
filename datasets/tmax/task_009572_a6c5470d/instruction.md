You are acting as a QA Engineer setting up a test environment for a new mathematical application. The team uses a proprietary stack-based "MathVM" to evaluate complex mathematical test cases. 

Currently, the MathVM emulator is written in Python, but it's too slow for our large-scale load tests. Your task is to translate this MathVM implementation into Go, verify its correctness, and run performance benchmarks to compare with the Python version.

Here are your instructions:

1. Analyze the existing Python implementation located at `/home/user/mathvm.py`. This script implements a simple stack-based emulator with `PUSH`, `ADD`, `SUB`, `MUL`, and `DIV` operations.
2. Initialize a new Go module named `mathvm` in `/home/user/mathvm`.
3. Translate the Python emulator logic into Go. Write your implementation in `/home/user/mathvm/vm.go`. It should export a function `Evaluate(program string) int` that behaves exactly like the Python version (using integer arithmetic).
4. Create a benchmark test in `/home/user/mathvm/vm_test.go` containing a standard Go benchmark function named `BenchmarkEvaluate`. This benchmark should run the `Evaluate` function using the contents of `/home/user/test_program.txt`.
5. Run your Go benchmark and save the terminal output to `/home/user/benchmark_results.txt`. Use standard Go benchmarking flags (e.g., `go test -bench=.`).
6. To verify correctness, create an entrypoint `/home/user/mathvm/main.go` that reads the file `/home/user/test_program.txt`, passes its contents to your `Evaluate` function, and writes the resulting integer to `/home/user/go_output.txt` (just the number, no extra text or newlines).

All necessary starting files (`/home/user/mathvm.py` and `/home/user/test_program.txt`) are already present in the environment.