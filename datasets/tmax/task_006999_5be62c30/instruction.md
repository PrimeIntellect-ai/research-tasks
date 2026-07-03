You are an operations engineer triaging an incident. A financial aggregation script running in production is producing incorrect total values, leading to discrepancies in downstream reporting.

The script is located at `/home/user/calc.py`. It reads a list of transaction amounts from `/home/user/data.txt`, calculates the total, and writes the sum to `/home/user/output.txt`.

However, the script has a few issues:
1. There is a dependency conflict in `/home/user/requirements.txt` preventing the environment from being set up properly.
2. The script contains an off-by-one error causing it to miss certain data points.
3. The script suffers from floating-point precision issues, causing inaccurate sums for decimal values.

Your task:
1. Resolve the dependency conflict in `/home/user/requirements.txt` and install the requirements using `pip install -r /home/user/requirements.txt`.
2. Fix the bugs in `/home/user/calc.py`. You must ensure that it calculates the exact decimal sum of all values in `/home/user/data.txt` without any floating-point precision loss. 
3. Run the script so that the exact correct total is written to `/home/user/output.txt`. 

The output in `/home/user/output.txt` should be the exact sum as a standard decimal number (e.g., `0.6`), with no trailing precision errors like `0.6000000000000001`.