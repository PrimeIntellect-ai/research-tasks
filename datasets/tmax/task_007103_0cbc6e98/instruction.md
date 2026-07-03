You are a support engineer investigating a bug reported by a key enterprise customer. They are using our C-based data processing utility, `sensor_aggregator`, to calculate the standard deviation of sensor telemetry data. Intermittently, the tool outputs `nan` (Not a Number) instead of a valid metric, causing downstream pipeline failures. 

The source code is located at `/home/user/sensor_aggregator.c`. 

Your objective is to diagnose, isolate, and fix this issue by following these steps:

1. **Fuzz Testing:** Write a fuzzer to generate various inputs (lists of floating-point numbers, one per line) to successfully trigger the `nan` output from the compiled `/home/user/sensor_aggregator` binary. The customer noted this tends to happen when base sensor values are very large with very small fluctuations.
2. **Delta Debugging / Minimization:** Once you find an input that triggers the `nan` bug, use delta debugging principles to minimize the input file. Reduce the input to the smallest number of lines that still reproduce the `nan` output on the original buggy binary. Save this minimized dataset to `/home/user/minimized_crash.csv`.
3. **Floating-Point Precision Repair:** Analyze `sensor_aggregator.c`. You will notice it uses a numerically unstable, naive formula for variance calculation which suffers from catastrophic cancellation. Rewrite the variance calculation in `sensor_aggregator.c` using a numerically stable algorithm (e.g., Welford's online algorithm or a two-pass approach). 
4. **Verification:** Recompile your fixed version using the provided `/home/user/Makefile`. Run your fixed binary against your `/home/user/minimized_crash.csv`. Save the standard output of this run to `/home/user/fixed_output.txt`.

Constraints:
- Do not change the input/output format of the C program. It must read line-by-line floats from a file and print a single float to stdout.
- The `/home/user/minimized_crash.csv` must trigger a `nan` on the *original* buggy binary.
- The `fixed_output.txt` must contain a valid, non-negative floating-point number.