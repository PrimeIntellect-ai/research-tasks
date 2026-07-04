**IT Support Ticket #9942**
**Subject:** `calc_metrics` tool is crashing on nightly data batch
**Priority:** High

Hi,

We are getting a crash (Segmentation Fault) in our daily metric aggregator tool. The code is located at `/home/user/calc_metrics/calc_metrics.c` and processes a CSV-like file containing mathematical data to calculate the harmonic mean of value sets and generate a histogram.

It was working fine until the latest `nightly.csv` drop, which seems to contain some edge-case formats or mathematical anomalies that break our assumptions. 

Here is what we need you to do:
1. Debug the `calc_metrics.c` program. You can use `gdb` to trace where the segmentation fault occurs when running against `/home/user/calc_metrics/nightly.csv`.
2. Fix the bugs in the C code. 
   - **Rule 1 (Format Parsing):** If a record has a count of `0`, it might not have a trailing semicolon or value list (e.g., `ID;0`). The program should handle this without crashing and return a mean of `0.0`.
   - **Rule 2 (Math/Memory Anomaly):** If the sum of the inverses in the harmonic mean calculation is exactly `0.0`, the resulting mean should be forced to `0.0` to avoid division-by-zero/Infinity propagation, which corrupts our histogram buckets.
3. Recompile the program.
4. Run the fixed program: `./calc_metrics nightly.csv output_fixed.csv`
5. Save the output. Automated tests will verify the exact contents of `/home/user/calc_metrics/output_fixed.csv`.

Thank you,
IT Support Team