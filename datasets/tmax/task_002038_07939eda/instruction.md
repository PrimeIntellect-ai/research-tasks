You are tasked with debugging a regression in a distributed sensor aggregation service.

Recently, the `aggregate.py` service has been crashing in production. The crashes only occur with specific edge-case telemetry data. We have captured a packet dump of the traffic during a crash in `/home/user/traffic.pcap`. 

The service is maintained in a Git repository located at `/home/user/sensor_aggregator`. The repository has around 200 commits. We know that the tag `v1.0` is a "good" state where the service did not crash, and the current `HEAD` (master branch) is a "bad" state where it does.

Your objectives:
1. **Network & Serialization Analysis:** Analyze `/home/user/traffic.pcap` to extract the UDP payloads destined for port 5000. The packets contain binary serialized telemetry data.
2. **Crash Reproduction & Fuzzing:** Identify which extracted payload causes `aggregate.py` to crash. The script accepts a hex-encoded payload string as a command-line argument: `python aggregate.py <hex_payload>`.
3. **Regression Bisection:** Use `git bisect` to find the exact commit that introduced the crash. 
4. **Numerical Instability Fix:** The crash is caused by a numerical instability bug (e.g., division by zero or domain error) introduced in the bad commit. Identify the bug and write a patched, crash-free version of the script to `/home/user/fixed_aggregate.py`. If the denominator evaluates to zero, you should safely return `0.0`.

**Deliverables:**
1. Save the full Git commit hash of the first bad commit to `/home/user/bad_commit.txt`.
2. Save the hex-encoded string of the payload that triggers the crash to `/home/user/poison_payload.txt`.
3. Save your patched python script to `/home/user/fixed_aggregate.py`.

*Note: You may use standard Python libraries, `scapy`, `tcpdump`, or any other tools available in standard Linux environments to complete this task.*