You are a Site Reliability Engineer (SRE) investigating an issue with our daily uptime reporting script.

We have a Python script located at `/home/user/uptime_monitor.py` that parses a container log file (`/home/user/container_logs.txt`) to calculate the daily SLA (Service Level Agreement) uptime percentage.

Currently, the script is failing for two reasons:
1. **Format Parsing Edge-Case:** The script crashes with a `ValueError` on certain lines. Some lines in the container logs have slight malformations (e.g., irregular spacing) that break the naive string splitting logic.
2. **Floating-Point Precision & Formula:** Even when the parsing bug is bypassed, the downtime accumulation suffers from IEEE 754 floating-point precision artifacts (e.g., adding `300.1` and `100.2` results in `400.29999999999995`), which causes our SLA metrics to be rejected by the downstream compliance system.

Your task:
1. Debug and fix the parsing logic in `/home/user/uptime_monitor.py` so it correctly extracts the `STATUS` and `DURATION_MS` regardless of extra whitespace between the timestamp, status, and duration.
2. Fix the floating-point arithmetic. The accumulated downtime must be exact (consider using Python's built-in modules for exact decimal arithmetic).
3. The total expected time for the period is exactly 24 hours (86,400,000 milliseconds). The SLA percentage formula is: `100.0 - ((total_downtime_ms / total_time_ms) * 100)`.
4. Once fixed, run the script and write the final calculated SLA to `/home/user/fixed_report.txt`.

The format of `/home/user/fixed_report.txt` must be exactly:
`SLA: <value>%`
Where `<value>` is rounded to exactly 6 decimal places (e.g., `99.999537`).

Do not change the names or locations of the input files. Ensure the final report is generated successfully.