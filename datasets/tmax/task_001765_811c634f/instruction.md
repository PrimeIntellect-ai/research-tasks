You are a Site Reliability Engineer investigating an anomalous uptime monitoring service. Our custom SLA tracker has recently started reporting severe precision degradation (our "Five 9s" SLA keeps drifting to 99.989% inexplicably), and the monitoring daemon is consuming excessive CPU overhead. 

The environment contains:
1. A main monitor script at `/home/user/monitor/uptime_tracker.py`. This script accumulates ping response times and calculates the overall SLA percentage. 
2. A vendored third-party ping library at `/app/vendored/pingspinner/`. The `uptime_tracker.py` script imports this locally to perform network checks. 

Your investigation indicates three distinct problems:
A. There is a precision loss issue in how `uptime_tracker.py` accumulates total uptime versus downtime across millions of micro-measurements.
B. An off-by-one boundary condition in the rolling window logic drops valid ping measurements.
C. A recent patch to the vendored `pingspinner` library introduced a severe performance regression. Using system call tracing, you should find why it's burning CPU while waiting for socket responses.

Your task:
1. Diagnose and fix the system call storm in `/app/vendored/pingspinner/core.py`.
2. Fix the off-by-one window boundary error in `/home/user/monitor/uptime_tracker.py`.
3. Fix the floating-point precision loss in `/home/user/monitor/uptime_tracker.py` so that it calculates the SLA metric flawlessly even with extreme variance in magnitudes.
4. Your fix will be evaluated by an automated script that simulates 1,000,000 fast-forwarded monitoring ticks. 

You must modify the existing code in `/home/user/monitor/uptime_tracker.py` and `/app/vendored/pingspinner/core.py` directly. Do not change the function signatures or the location of the files. The system will evaluate the final performance and precision using a predefined metric. Ensure your code is completely optimized.