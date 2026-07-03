You are an SRE monitoring the uptime of our critical infrastructure. We have an automated script that calculates uptime by parsing heartbeat packets (ICMP echo replies) from a network capture (`.pcap`) file. Our SLA requires an uptime of 99.999%, and intermediate assertions in our pipeline validate that the computed uptime meets this threshold.

Recently, the uptime calculation script in our repository started failing its internal assertions, reporting an uptime slightly below the SLA despite no actual outages occurring. We suspect a recent code change introduced a floating-point precision regression when aggregating micro-outages (very small packet delays).

Your task:
1. Navigate to the Git repository at `/home/user/uptime_monitor`.
2. Use Git bisection to find the exact commit that introduced the regression. The last known good commit is tagged `v1.0`. The script `check_uptime.py` contains an `assert` statement that will fail if the regression is present.
3. Write the full 40-character Git commit hash of the bad commit to `/home/user/bad_commit.txt`.
4. Fix the floating-point precision issue in `check_uptime.py` so that it calculates the uptime accurately without losing precision from accumulating many tiny floating-point values. (Hint: Python's standard library has tools for precise float summation).
5. Run your fixed `check_uptime.py` against the packet capture located at `/home/user/uptime_monitor/heartbeats.pcap`.
6. Write the final computed uptime percentage, rounded to exactly 5 decimal places (e.g., `99.99912`), to `/home/user/final_uptime.txt`.

Ensure your fix passes the assertion naturally without just hardcoding the expected answer or modifying the assertion itself. You may use `scapy` (installed in the environment) if you need to inspect the pcap reading logic, though the bug is specifically in the mathematical aggregation.