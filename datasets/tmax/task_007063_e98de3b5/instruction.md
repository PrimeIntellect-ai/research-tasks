You are an IT support technician responding to Ticket #4489. 

A user has reported issues with a scientific data summarizer tool located at `/home/user/ticket_4489/summarize.py`. The tool processes an array of floating-point numbers. It calculates a total sum using a pure Python function, and processes a fast-path moving average using a precompiled shared library `/home/user/ticket_4489/libcalc.so`. 

The user reports two distinct bugs:
1. **Precision Error**: The total sum reported by the Python function is often slightly off due to floating-point precision issues (e.g., adding many small floats).
2. **Intermittent Crashes**: The tool sometimes segmentation faults when passing data to the `libcalc.so` shared library. The source code for the C library is lost. You will need to inspect the binary or its behavior, and then fix the boundary condition or off-by-one error in how `summarize.py` invokes it.

Your tasks are:
1. **Fix the Python precision issue**: Modify `summarize.py` to calculate the exact floating-point sum without precision loss.
2. **Fix the boundary condition**: Determine why `libcalc.so` is crashing and modify the C-types wrapper call in `summarize.py` to prevent the off-by-one access while still processing all elements correctly.
3. **Write a Fuzzer**: Create `/home/user/ticket_4489/fuzzer.py` that generates random lists of floats (lengths between 5 and 50) and calls the functions in `summarize.py` 1000 times to ensure no crashes occur.
4. **Create a Regression Test**: Create `/home/user/ticket_4489/test_regression.py`. It should verify that `sum_values([0.1]*10)` equals exactly `1.0` (which previously failed) and verify that the C-library function does not crash on an array of size 10.
5. **Log the Resolution**: Once complete, write a file `/home/user/ticket_4489/resolution.txt` containing the word `RESOLVED`.

Constraints:
- Do not modify `libcalc.so` directly (you don't have the source).
- Only use standard Python libraries.