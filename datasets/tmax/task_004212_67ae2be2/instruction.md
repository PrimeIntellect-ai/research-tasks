You are a performance engineer tasked with debugging a custom network packet profiling application located at `/home/user/netprofiler`. The application is supposed to parse a packet capture file, calculate performance metrics, and identify traffic patterns. 

However, the application is currently broken in several ways:
1. **Build/Environment Failure**: Attempting to install the application using `pip install .` inside `/home/user/netprofiler` fails due to a misconfiguration in the project's dependency specifications. You need to diagnose and fix the build configuration so the package installs successfully.
2. **Formula Implementation Error**: The core metric calculation in `/home/user/netprofiler/netprofiler/metrics.py` calculates the Mean Inter-Arrival Jitter. The current implementation is mathematically incorrect. The correct formula for Mean Inter-Arrival Jitter here should be the average of the absolute differences between consecutive packet inter-arrival times. 
   *(Let $T_i$ be the timestamp of the $i$-th packet. The inter-arrival time is $I_i = T_i - T_{i-1}$. The jitter is the average of $|I_j - I_{j-1}|$ for all available valid pairs).*
3. **Execution & Forensics**: Once fixed, run the tool on the provided capture file at `/home/user/capture.pcap`. 

Write a python script at `/home/user/run_analysis.py` that imports the fixed `netprofiler` package, parses `/home/user/capture.pcap`, and generates a JSON report at `/home/user/report.json`.

The JSON file must have exactly this structure:
```json
{
  "total_packets": 0,
  "top_src_ip": "1.2.3.4",
  "mean_jitter": 0.000000
}
```
*Note: `top_src_ip` should be the IPv4 address that sent the most packets.*