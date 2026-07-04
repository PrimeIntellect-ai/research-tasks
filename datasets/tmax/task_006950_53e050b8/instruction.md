You are a support engineer working on a mathematical data processing pipeline. Customers have reported that our batch processing script, which calculates the Collatz conjecture stopping times for large datasets, is crashing intermittently under high load. Furthermore, it occasionally fails deterministically on specific data batches.

The pipeline consists of a C++ worker (`/home/user/math_worker.cpp`) that performs the calculations concurrently, and a Python wrapper (`/home/user/parser.py`) that feeds data to the worker and parses its standard output. 

Your tasks:
1. **Intermittent Failure Diagnostics**: The pipeline intermittently crashes with a format parsing error when processing large batches due to thread contention in the C++ worker. Isolate the root cause (output interleaving due to missing synchronization).
2. **Format Edge-Case Repair**: There is also a specific mathematical edge-case in `/home/user/data_batch.txt` that consistently crashes the Python parser because the C++ worker outputs a different format for invalid domains (e.g., non-positive integers).
3. **Test Minimization**: Use delta debugging to find the exact line in `/home/user/data_batch.txt` that triggers the deterministic edge-case parsing failure. Save this single input value to a file named `/home/user/minimal_repro.txt`.
4. **Fix the C++ Worker**: Modify the C++ code to prevent output interleaving (e.g., by adding a mutex around standard output). Save the fixed code as `/home/user/math_worker_fixed.cpp` and compile it to `/home/user/math_worker_fixed`.
5. **Fix the Python Parser**: Update the Python script so that if it encounters the C++ worker's specific "Error:" output format for invalid mathematical domains, it simply skips the line instead of raising an exception. Save this as `/home/user/parser_fixed.py`.
6. **Intermediate State Tracing**: To prove your diagnosis of the concurrent interleaving issue, capture a snippet of the raw, malformed C++ output (where two output lines are jumbled together, e.g., `NumbeNumber: ...`) and save it to `/home/user/interleaved_trace.log`.

**System State:**
- The C++ source is at `/home/user/math_worker.cpp`. You should compile the original with `g++ -std=c++11 -pthread /home/user/math_worker.cpp -o /home/user/math_worker` to test it.
- The Python script is at `/home/user/parser.py`.
- The input dataset is at `/home/user/data_batch.txt` (contains 10,000 integers).

**Success Criteria:**
- `/home/user/minimal_repro.txt` must contain exactly the single integer that causes the deterministic crash.
- `/home/user/math_worker_fixed` must be compiled and not exhibit interleaved stdout when run with many inputs.
- `/home/user/parser_fixed.py` must successfully process the entire `/home/user/data_batch.txt` without crashing.
- `/home/user/interleaved_trace.log` must contain at least one line demonstrating the stdout race condition.