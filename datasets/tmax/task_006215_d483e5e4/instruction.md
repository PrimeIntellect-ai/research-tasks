You are an SRE investigating a failing monitoring daemon. 

We have a C program located at `/home/user/uptime_monitor.c` that parses response time metrics from `/home/user/response_times.txt`. It computes the running mean and standard deviation of these response times to trigger alerts if the variance gets too high. 

Recently, our latency baseline shifted to around 1,000,000 microseconds, and the daemon started crashing with an assertion failure:
`uptime_monitor: uptime_monitor.c:XX: main: Assertion '!isnan(stddev)' failed.`
Aborted (core dumped)

Your task is to:
1. Identify the numerical instability in `/home/user/uptime_monitor.c` causing the standard deviation to calculate as `NaN`. (Hint: The naive variance calculation formula suffers from catastrophic cancellation with large floating-point numbers).
2. Modify the C code to calculate the variance and standard deviation in a numerically stable way (for example, using Welford's online algorithm or a two-pass mean-centering approach).
3. Add an intermediate assertion to the code right before the `sqrt()` call to validate the variance: `assert(variance >= 0.0);`
4. Compile the fixed code to `/home/user/uptime_monitor_fixed`. (Remember to link the math library).
5. Run the fixed binary and redirect its standard output to `/home/user/fixed_stats.txt`.

The final state of the system must contain the fixed source code, the compiled binary, and the `/home/user/fixed_stats.txt` file containing the successful output.