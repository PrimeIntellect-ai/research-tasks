You are a Site Reliability Engineer (SRE) investigating an issue with our custom latency monitoring daemon. 

The daemon tracks response times from our internal services. To detect anomalies, it maintains a running variance of the latency. Recently, the variance metric has been reporting `NaN` (Not a Number), causing our downstream serialization to fail and breaking the telemetry dashboard.

The source code for the metric calculator is located at `/home/user/uptime_monitor.c`. It reads the current state (count, sum of latencies, sum of squared latencies) from a file, updates it with a new latency provided as a command-line argument, and calculates the variance.

Currently, the C code uses a naive variance formula: `Var(X) = E[X^2] - (E[X])^2`. Due to catastrophic cancellation (precision loss) when response times are large and stable, this formula occasionally produces a negative number. Taking the square root of this negative number yields `NaN`.

Your task:
1. Fix the precision loss issue in `/home/user/uptime_monitor.c`. You may either implement Welford's online algorithm or add a safeguard to prevent negative variance before the square root is applied (e.g., if the calculated variance is `< 0.0`, treat it as `0.0`).
2. Construct a regression test. Create a script at `/home/user/regression_test.sh` that compiles `/home/user/uptime_monitor.c`, creates a dummy state file `/home/user/state.txt` with values that trigger the bug, runs the compiled executable, and verifies that `NaN` is no longer output. The script should exit with code 0 on success and 1 on failure.
3. Once fixed, run the executable with the provided bad state. Create the file `/home/user/state.txt` with exactly this content:
   `1000 1000000000.0 1000000000000000.0`
   (Format is: `count sum sum_sq`).
   Then run your compiled executable with a new latency measurement of `1000000.0`.
4. Save the standard output of that run (which prints the new variance) into `/home/user/fixed_variance.log`.

Ensure your C code compiles correctly with standard GCC (e.g., `gcc -O2 uptime_monitor.c -lm -o uptime_monitor`).