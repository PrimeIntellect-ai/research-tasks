A regression has been introduced in our calculation engine repository at `/home/user/repo` that causes a severe precision loss in the `calculate_metrics()` function inside `math_ops.py`. 

The test data containing the high-precision expected value was lost, but a memory dump of the old test runner was saved at `/home/user/memory.dump`. 

Your tasks are:
1. Analyze `/home/user/memory.dump` to extract the high-precision expected string value. It is stored somewhere in the binary dump in the format `EXPECTED_METRIC_VALUE=<value>`.
2. Write a Python test script to evaluate `calculate_metrics()` from `math_ops.py`. A commit is "good" if the string representation of the returned value matches the expected metric value up to at least 15 decimal places. It is "bad" if there is precision loss.
3. Use Git bisection in `/home/user/repo` to find the exact commit hash that introduced the precision loss. The very first commit in the repository is known to be good, and the current `HEAD` is known to be bad.
4. Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.