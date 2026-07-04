You are a Site Reliability Engineer investigating a false alert regarding our service's uptime and network stability. 

Our monitoring script periodically analyzes network heartbeat packets (captured in a pcap file) to compute the "jitter" (variance of inter-arrival times) of our heartbeat pings. If the jitter exceeds a certain threshold, the SLA metric drops, triggering an alert. Recently, the dashboard started reporting severe SLA drops, even though there are no actual network issues. 

We suspect a recent code change introduced a floating-point precision error in the jitter calculation. The timestamps are standard Unix epoch times (e.g., 1700000000.xxx), and a naive variance calculation on these large floating-point numbers is likely causing catastrophic cancellation.

Your tasks:
1. Navigate to the git repository at `/home/user/sla-monitor`.
2. Use `git bisect` to identify the exact commit that introduced the floating-point precision bug. The script `check_sla.py` processes `test_heartbeats.pcap` and will exit with a non-zero code if the jitter calculation yields an invalid or unexpectedly high value (the false alert). The oldest commit in the repository is known to be good, and `HEAD` is bad.
3. Fix the floating-point precision issue in `check_sla.py`. You should implement a numerically stable variance calculation (e.g., Welford's algorithm, using `statistics.variance`, or subtracting the first timestamp as a mean-shift before squaring).
4. After fixing the code, run the script against the production capture: `python3 check_sla.py prod.pcap > /home/user/final_jitter.txt`.
5. Create a file at `/home/user/resolution.txt` containing exactly two lines:
   - Line 1: The full 40-character commit hash of the bad commit.
   - Line 2: The corrected jitter value for `prod.pcap` (just the number, as outputted by your fixed script).

Note: You can use `scapy` to read the pcap files (it is pre-installed). The timestamps should be extracted exactly as they appear in the packets.