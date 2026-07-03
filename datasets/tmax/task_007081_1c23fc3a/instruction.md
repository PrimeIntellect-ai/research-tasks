You are a software engineer tasked with porting and testing a C++ financial metrics CLI tool to run in a minimal container environment. The tool reads a sequence of data points, applies a strict rate limit to incoming requests, and computes a Simple Moving Average (SMA). 

However, the current state of the codebase in `/home/user/metrics_tool` is incomplete and broken:
1. **Broken Build:** The `Makefile` has syntax or dependency errors and fails to compile the C++ source code.
2. **Incomplete Numerical Algorithm:** The SMA algorithm in `calculator.cpp` is missing its implementation.
3. **Missing Tests:** There is no automated way to test the request validation (rate limiting) and numerical output.

Your objectives:

1. **Fix the Makefile:** Ensure that running `make` in `/home/user/metrics_tool` correctly builds the executable named `metrics_tool`.
2. **Implement the Algorithm:** Complete the `double compute_sma(double new_value)` function in `calculator.cpp`. The function must compute the simple moving average of the last 3 values (window size = 3). If fewer than 3 values have been processed, it should return the average of the available values. (e.g., if inputs are 10, 20, the SMA is 15. If inputs are 10, 20, 30, the SMA is 20. If next is 40, the SMA of 20, 30, 40 is 30).
3. **Write a Test Script:** Create a Python script at `/home/user/test_script.py` that acts as an integration test. 
   The `metrics_tool` reads from standard input where each line is formatted as `timestamp_sec,value`. It outputs `timestamp_sec,RESULT` where `RESULT` is either the calculated SMA (up to 2 decimal places) or `RATE_LIMIT_EXCEEDED` if more than 2 requests are sent within the same timestamp second.
   
   Your Python script must:
   - Programmatically run `/home/user/metrics_tool/metrics_tool`.
   - Feed it the following exact input via stdin:
     ```
     1,10.0
     1,20.0
     1,30.0
     2,40.0
     ```
   - Capture the stdout of the tool.
   - Verify the output perfectly matches the expected behavior:
     - The first request (10.0) should succeed (SMA = 10.0).
     - The second request (20.0) should succeed (SMA = 15.0).
     - The third request (30.0) should be rejected (RATE_LIMIT_EXCEEDED) because the rate limit is 2 requests per second. (Note: rejected requests DO NOT affect the SMA state).
     - The fourth request (40.0) should succeed (SMA = 23.33) -> average of 10.0, 20.0, and 40.0.
   - If the output is perfectly correct, the script must print exactly `ALL_TESTS_PASS` to standard output. Otherwise, it should print `FAIL`.

4. **Run the Test:** Execute your test script and redirect its output to `/home/user/test_results.log`.

Do not modify the `main.cpp` or `rate_limiter.cpp` files. Only modify `Makefile`, `calculator.cpp`, and create `test_script.py`.