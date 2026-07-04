You are an engineer tasked with setting up a polyglot build and test system from scratch. We have a data processing pipeline that relies on a fast C program for algorithmic computation, a Go service to handle concurrent orchestration, and a Python test harness to tie it all together.

Unfortunately, the previous developer left the system in a broken state. You need to repair the C build, complete the Go concurrency logic, and write a Python integration test script to orchestrate the pipeline.

Here is the current state and what you need to do:

1. **Fix the C component** (`/home/user/polyglot/core/`):
   - There is a `compute.c` file that calculates the sum of all prime numbers up to and including a given integer `N` passed as a command-line argument. It prints the integer result to stdout. There is a logical bug in the prime calculation (it currently fails to include `N` if `N` itself is prime due to a loop boundary condition).
   - The `Makefile` in the same directory is broken. It fails to compile the `compute` binary. Fix the `Makefile` so that running `make` successfully produces an executable named `compute`.

2. **Complete the Go component** (`/home/user/polyglot/worker/`):
   - The file `main.go` is supposed to read a JSON array of integers from standard input (e.g., `[10, 50, 100]`).
   - It must use Go concurrency patterns (goroutines and channels) to process these integers concurrently. For each integer, it should use `os/exec` to call the compiled C binary (`/home/user/polyglot/core/compute N`) and parse the output.
   - It must output a JSON object to standard output mapping the input string to the sum of primes string (e.g., `{"10": 17, "50": 328, "100": 1060}`).
   - Ensure the Go program compiles correctly with `go build -o worker main.go`.

3. **Write the Python Build and Test System** (`/home/user/polyglot/build_and_test.py`):
   - Write a Python 3 script that orchestrates the entire process.
   - It should first run `make` in `/home/user/polyglot/core/`.
   - Then run `go build -o worker main.go` in `/home/user/polyglot/worker/`.
   - Next, it must execute the Go `worker` binary, passing `[10, 20, 30]` to its standard input.
   - It must verify the output against the expected correct sums (17, 77, and 129 respectively).
   - Finally, your Python script must output the test results to a JSON file at `/home/user/polyglot/test_results.json` with the exact following schema:
     ```json
     {
       "c_build_ok": true,
       "go_build_ok": true,
       "integration_passed": true
     }
     ```
     (Set values to `false` if any step fails, but a fully correct solution should result in all `true`).

You may write your Python script however you see fit using standard library modules (e.g., `subprocess`, `json`).