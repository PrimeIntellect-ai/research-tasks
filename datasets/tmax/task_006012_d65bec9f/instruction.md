You are an engineer stepping in to investigate a memory leak and a build failure in a long-running mathematical data processing service.

The service is located in `/home/user/math_service/`.

Here are the issues you need to resolve:
1. **Build Failure**: The service has a Cython optimization module (`fast_math.pyx`). The build script (`setup.py`) is failing when you run `python3 setup.py build_ext --inplace`. Diagnose the build failure and fix `setup.py` so the extension compiles successfully.
2. **Format Parsing Edge-Case**: The service reads incoming sensor data from `/home/user/math_service/data.txt`. The parsing function in `parser.py` crashes or silently fails when it encounters lines with trailing commas or irregular whitespace (e.g., `12.5, 14.2, `). Fix `parser.py` so it correctly extracts all valid floats from these poorly formatted lines, ignoring empty fields.
3. **Memory Leak & Boundary Condition**: The main processor in `service.py` maintains a rolling window of recent calculations. However, memory usage grows indefinitely. Inspect `service.py`, find the boundary condition/off-by-one logic error in the caching or rolling buffer mechanism that prevents old records from being evicted, and fix it. 

After you have fixed all three issues:
1. Rebuild the Cython extension: `python3 setup.py build_ext --inplace`
2. Run the test script: `python3 test_service.py`. This script will verify the build, parse the test data, and check that memory does not leak over 10,000 iterations.
3. The test script will automatically write a success log to `/home/user/math_service/success.log` if everything passes. 

Once finished, simply ensure that `/home/user/math_service/success.log` exists and contains the word "PASS".