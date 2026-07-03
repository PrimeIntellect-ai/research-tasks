You have inherited an unfamiliar project that relies on a proprietary statistical anomaly scoring engine, provided as a compiled binary at `/app/oracle_bin`. This binary takes a single string of uppercase alphanumeric characters as a command-line argument and outputs a single integer representing the "anomaly score".

Your predecessor was attempting to rewrite this logic in Python to remove the dependency on the binary, but they left the company before finishing. Their work is located in `/home/user/legacy/`.

Currently, the legacy setup is broken:
1. `pip install -r /home/user/legacy/requirements.txt` fails due to a dependency conflict (some ancient statistical libraries conflict with each other).
2. The python script `/home/user/legacy/scorer.py` crashes with a `RecursionError` when run.
3. Even when the crash is bypassed, the outputs exhibit a statistical anomaly—they drift significantly from the outputs of `/app/oracle_bin`.

Your task:
1. Debug the dependency conflict to get the environment working (if you choose to use the legacy code).
2. Fix the recursion and loop termination issues in the Python rewrite.
3. Investigate the statistical anomalies in the legacy code's logic by comparing its output against `/app/oracle_bin` (treat the binary as the absolute source of truth).
4. Write a final, perfected Python script at `/home/user/solution.py` that takes a single string as a command-line argument and prints the exact same integer output as `/app/oracle_bin` for any given uppercase alphanumeric string.

Your solution must perfectly match the binary's output for any valid string. We will verify your solution by fuzzing `/home/user/solution.py` against `/app/oracle_bin` with hundreds of random inputs.