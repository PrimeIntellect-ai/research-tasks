You are a DevOps engineer analyzing a nightly job failure. 

A bash script located at `/home/user/network_analyzer.sh` is scheduled to process network packet capture summaries from `/home/user/pcap_summary.log` to calculate total session throughputs. Unfortunately, the script crashed last night, leaving behind a trace execution log at `/home/user/trace.log`.

Your objectives:
1. Examine `/home/user/trace.log` to determine the intermediate state of the variables right before the script crashed.
2. Identify the mathematical formula error in `/home/user/network_analyzer.sh`. The bug occurs because some sessions start and end in the exact same millisecond, causing a division by zero. 
3. Correct the formula implementation in the bash script. The calculation for `throughput` should treat any `duration` of `0` as `1` millisecond to avoid crashes, while calculating `bytes / duration`.
4. After correcting the script, run it. The script is configured to write its final output to `/home/user/result.txt`.
5. Copy the final calculated number from `/home/user/result.txt` into a new file `/home/user/solution.txt`. 

File locations:
- Script: `/home/user/network_analyzer.sh`
- Log data: `/home/user/pcap_summary.log`
- Trace: `/home/user/trace.log`
- Final Verification File: `/home/user/solution.txt` (must contain only the final integer value).