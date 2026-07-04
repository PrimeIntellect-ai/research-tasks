**Ticket Number:** IT-REQ-8442
**Subject:** Intermittent crashes in legacy trajectory stats module
**Assignee:** IT Support / Tier 3

**Description:**
Hello,

Our physics team uses an old compiled Python utility, `legacy_stats.pyc`, located at `/home/user/legacy_stats.pyc`. It computes the mean and population standard deviation for a set of data points. We lost the source code years ago.

Recently, the team reported that the utility intermittently crashes with a `ValueError: math domain error` when processing data streams with very little variation but extremely large base magnitudes. Other times, it returns `0.0` or inaccurate numbers for the standard deviation. We suspect this is due to precision loss / catastrophic cancellation in how the variance formula was originally implemented.

Your task is to:
1. Reverse engineer the bytecode in `/home/user/legacy_stats.pyc` to understand the flawed naive variance formula it uses.
2. Reproduce the intermittent failure by creating a file `/home/user/crash_input.txt` containing a single line of comma-separated floating-point numbers. When these numbers are passed as a list of floats to `legacy_stats.calculate_metrics(data)`, it must trigger the `ValueError` (due to the variance becoming negative before the square root).
3. Write a corrected implementation in `/home/user/fixed_stats.py`. This script must expose a function `calculate_metrics(data: list[float]) -> tuple[float, float]` that calculates the mean and population standard deviation, but uses the numerically stable **two-pass algorithm** (i.e., calculating the mean first, then computing the mean of the squared differences from the mean). Do not use the `statistics` module; implement the math directly to ensure zero dependency issues.
4. Create a runner script `/home/user/run_trace.py` that reads the numbers from `/home/user/crash_input.txt`, passes them to your fixed `calculate_metrics` function in `fixed_stats.py`, and writes the resulting standard deviation (as a plain float) to `/home/user/fixed_output.txt`.

**Deliverables Summary:**
- `/home/user/crash_input.txt` (Triggers `ValueError` in `legacy_stats`)
- `/home/user/fixed_stats.py` (Stable implementation of `calculate_metrics(data)`)
- `/home/user/run_trace.py` (Script that generates the output)
- `/home/user/fixed_output.txt` (The accurate standard deviation for your crash input)

Good luck!