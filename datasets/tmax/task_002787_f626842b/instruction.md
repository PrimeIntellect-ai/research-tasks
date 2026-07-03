You are a performance engineer analyzing a mathematical sequence evaluator. Recently, a benchmarking session failed due to intermittent timeouts, and the input sanitization script was accidentally deleted.

Your objectives:

1. **Recover the Sanitization Logic**
   The script `sanitize_input.py` was accidentally deleted but is still available in the user's trash (`/home/user/.local/share/Trash/files/sanitize_input.py`). Recover it to `/home/user/sanitize_input.py`. This script contains the exact logic needed to handle corrupted, malformed, and anomalous numerical inputs from our data streams.

2. **Fix the Vendored Package**
   The core sequence evaluation is performed by a vendored library located at `/app/complex_collatz-0.1`. 
   During profiling, you noticed that the sequence evaluation intermittently hangs (infinite loop) for specific integers. 
   Analyze `/app/complex_collatz-0.1/core.py`, identify the root cause of the loop non-termination, and fix the package. You must modify the source code in place to ensure it correctly computes the mathematical sequence without hanging.

3. **Create the CLI Evaluator**
   Write a standalone Python script at `/home/user/fast_collatz.py` that takes a single string argument from the command line.
   Your script must:
   - Import the recovered `sanitize_input` module to clean the raw command-line string into a valid integer.
   - Use the fixed `complex_collatz` package to compute the sequence termination length.
   - Print *only* the resulting integer to standard output.

Example expected usage:
`python3 /home/user/fast_collatz.py "  14,, "` -> Outputs a single integer.

Ensure your implementation in `fast_collatz.py` is bit-exact equivalent to our reference implementation. An automated test will randomly fuzz your `fast_collatz.py` with hundreds of inputs and assert that its output perfectly matches our hidden oracle.