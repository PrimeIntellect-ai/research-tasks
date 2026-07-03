As a Site Reliability Engineer, I need your help investigating a critical issue with our internal uptime calculation tool, `uptime_calc`. Over the last few days, our monitoring dashboards have been showing bizarre statistical anomalies in our SLA calculations. 

I've taken a screenshot of the dashboard showing the expected SLA thresholds versus the current incorrect calculations. You can find this screenshot at `/app/uptime_graph.png`. Please extract the target 99.99% uptime representation value from this image—it will give you a clue about the magnitude of the floating-point precision error we're dealing with.

The source code for the calculation tool is located in a git repository at `/home/user/uptime_repo`. We know that a recent commit introduced a regression that causes floating-point precision errors when calculating long-term uptime percentages over large arrays of sensor ping data.

Your task is to:
1. Understand the codebase in `/home/user/uptime_repo`.
2. Use `git bisect` to identify the commit that introduced the floating-point regression. The commit `v1.0` is known to be good, and the `HEAD` is known to be bad.
3. Fix the floating-point precision issue in `src/uptime_calc.c` so that the uptime aggregation works correctly without losing precision for large datasets. You will likely need to change the accumulation strategy (e.g., Kahan summation or using `double` in specific aggregation loops).
4. Build the fixed tool. The repository has a `Makefile`. Running `make` will produce an executable at `/home/user/uptime_repo/build/uptime_calc`.

When you are finished, ensure the compiled binary at `/home/user/uptime_repo/build/uptime_calc` correctly processes a stream of space-separated ping latency floats from standard input and outputs a single 64-bit float representing the aggregate uptime percentage.

We will verify your solution by fuzzing your compiled binary against a known-good, stripped reference oracle.