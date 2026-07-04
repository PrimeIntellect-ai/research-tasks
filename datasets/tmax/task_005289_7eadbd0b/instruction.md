You are an IT support technician investigating a suspicious network activity ticket. A customer reported a potential data exfiltration event, but their internal log analysis script is returning incomplete results and missing the anomaly.

You have been provided with:
1. `/home/user/network_capture.txt`: A text-based packet capture log (similar to `tcpdump` output) representing recent traffic.
2. `/home/user/analyze.py`: A Python script written by the customer to calculate the total bytes received by each destination IP and identify the top receiver.

Your tasks are:
1. Investigate `/home/user/analyze.py`. There is a boundary condition / off-by-one error preventing it from processing the entire capture log, which causes it to miss the anomalous data exfiltration.
2. Fix the off-by-one error in `/home/user/analyze.py`.
3. Run the corrected script on `/home/user/network_capture.txt` to identify the statistical anomaly (the destination IP that actually received the most data).
4. Save the exact output of the fixed script to `/home/user/ticket_resolution.txt`. The format must be exactly `IP,TotalBytes` (e.g., `10.0.0.5,8500`).

Ensure your fixed Python script prints ONLY the anomalous IP and its total byte count in the specified format, and that the output is properly redirected or copied to `/home/user/ticket_resolution.txt`.