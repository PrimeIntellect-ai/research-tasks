You are acting as a DevOps engineer tasked with resolving an issue in a C++ log analysis tool. 

Our metrics processing pipeline has been failing recently. The tool, located at `/home/user/log_analyzer.cpp`, reads a custom system log and computes summary statistics. However, three distinct issues have been reported:

1. **Catastrophic Cancellation / Numerical Instability**: The variance of the response times is occasionally resulting in negative values or `NaN` due to the use of a mathematically naive variance formula. Response times are tightly clustered around a large base value (e.g., 10000.xxx ms).
2. **Encoding Failures**: The log contains hex-encoded payload strings. The current custom hex decoding function is throwing exceptions or returning garbage data because it incorrectly handles the case (uppercase vs. lowercase) of hex characters.
3. **Off-by-one / Boundary Condition**: The tool consistently reports exactly one less log entry than it should. The line parsing logic is ignoring either the first or the last line improperly.

Your task:
1. Review and fix the bugs in `/home/user/log_analyzer.cpp`.
2. Ensure you implement a numerically stable algorithm for computing the variance (e.g., Welford's algorithm or a proper two-pass algorithm using `double` precision).
3. Fix the hex decoding to handle both `A-F` and `a-f` alongside `0-9`.
4. Fix the loop/boundary condition so every single valid line in the log file is processed.
5. Compile the program using standard tools (e.g., `g++ -O2 -std=c++17 -o log_analyzer log_analyzer.cpp`).
6. Run the compiled tool against the provided log file `/home/user/system.log`. The tool takes two arguments: the input log file and the output JSON file.
7. Save the output to `/home/user/analysis_results.json`.

The log file has already been generated at `/home/user/system.log`.

The final `/home/user/analysis_results.json` should contain the exact output produced by the fixed tool. We will verify the `total_entries`, `decoded_bytes_count`, and the `variance` fields.