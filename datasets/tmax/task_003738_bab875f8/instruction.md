You are an IT support technician handling an escalated ticket. 

**Ticket #8842:**
"Our Go-based metrics aggregator service is crashing. It parses latency metrics from our container logs and calculates the standard deviation. We recently upgraded our containers, and the baseline latency increased to around 100,000,000 ns (with minor fluctuations). Since then, the service panics, complaining about a negative variance. Standard deviation requires a positive variance, but somehow the math is yielding negative numbers!"

**Workspace Details:**
- Go source code: `/home/user/aggregator.go`
- Container metrics log: `/home/user/container_metrics.log`

The original author used a naive single-pass formula to calculate the variance: `Variance = (Sum of Squares / Count) - (Mean * Mean)`. Due to the large base values and small differences in the recent logs, floating-point precision loss (catastrophic cancellation / numerical instability) is causing the calculated variance to become negative, triggering the panic.

**Your Task:**
1. Inspect the stack trace and code in `/home/user/aggregator.go`.
2. Diagnose and fix the floating-point precision issue by updating the variance calculation. You must implement a mathematically stable approach (like Welford's online algorithm or a stable two-pass variance calculation) to compute the population variance.
3. Run your fixed Go program against `/home/user/container_metrics.log`.
4. The program is already set up to write the resulting standard deviation to `/home/user/result.txt`. Ensure the output is formatted to exactly 6 decimal places (e.g., `0.123456`) and nothing else.

You have full access to the terminal to compile, run, and debug the Go code.