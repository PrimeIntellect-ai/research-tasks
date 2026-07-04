I am a developer trying to debug a failing build in our mathematical utilities library. The build fails during the test phase because of issues in `/home/user/math_build/factorizer.py`. 

The `factorizer.py` script is supposed to take a list of integers, compute their prime factors concurrently using threading, and return a deterministically sorted, base64-encoded JSON string of the results. However, there are multiple issues:
1. **Mathematical/Boundary Error**: The factorization logic fails for squares of prime numbers (e.g., 9, 25, 49). It returns the number itself instead of its prime factors.
2. **Concurrency Bug**: When processing many numbers, the results list is often missing entries due to a race condition in how the threads update the shared `results` list.
3. **Serialization/Encoding Bug**: The serialization step is throwing an encoding error or generating malformed output when handling the integer data types.

Your tasks:
1. Debug and fix `/home/user/math_build/factorizer.py` so that it correctly computes prime factors, safely handles concurrent updates, and properly serializes the sorted JSON list to a base64 UTF-8 string.
2. Construct a regression test script at `/home/user/regression_test.py` that imports `process_numbers` from `factorizer`. The script must call `process_numbers([4, 9, 25, 49, 121])` and use Python `assert` statements to validate the intermediate structures and the final base64 string against the expected mathematical truth.
3. Run your regression test. If it passes without `AssertionError`, echo the final base64 encoded string to `/home/user/build_success.log`.

Do not change the function signatures or the module name. You can use standard Python libraries.