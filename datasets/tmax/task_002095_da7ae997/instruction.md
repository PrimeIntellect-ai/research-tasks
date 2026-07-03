You are an IT support technician investigating an escalated ticket from the data science team. 

**Ticket Details:**
"Our sensor pipeline is suddenly dropping over 90% of incoming data. Service A sends UDP packets containing float values to Service B (the anomaly detector). Service B is supposed to reject outliers based on a rolling Z-score (rejecting values more than 3 standard deviations from the mean). However, after the first few dozen packets, it starts rejecting almost perfectly normal data. We suspect a statistical math error or logic bug in the anomaly detector, but we need you to prove it by reconstructing the timeline and fixing the code."

**Environment Setup & Files Provided:**
You have the following files in `/home/user/ticket/`:
*   `traffic.pcap`: A network packet capture of the UDP traffic between Service A (port 5000) and Service B (port 5001). The payloads are simply UTF-8 encoded float strings.
*   `service_a.log`: Log from the sender, containing timestamps and the payload sent.
*   `service_b.log`: Log from the receiver, logging when a value was accepted or rejected.
*   `detector.py`: The anomaly detection logic used by Service B. It implements Welford's online algorithm for calculating rolling variance and mean.
*   `run_pipeline.py`: A script that parses `traffic.pcap`, feeds the payloads in order to the `AnomalyDetector` from `detector.py`, and writes the results.

**Your Tasks:**
1.  Analyze `traffic.pcap` and the log files to reconstruct the timeline and identify precisely when and why the statistical rejection goes off the rails. You may install any tools you need (e.g., `scapy`, `tshark`) to inspect the PCAP.
2.  Investigate `detector.py`. Find the mathematical/statistical bug in how the rolling standard deviation or Z-score is computed.
3.  Fix the bug in `/home/user/ticket/detector.py`. Do not change the function signatures or class names.
4.  Once fixed, run `python /home/user/ticket/run_pipeline.py`. 

The `run_pipeline.py` script will automatically generate `/home/user/ticket/resolution.json`. This file will contain the final count of accepted packets and the final computed mean and standard deviation.

The automated verification process will read `/home/user/ticket/resolution.json` to verify that the bug was fixed and the correct statistical calculations were restored.