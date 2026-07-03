You are tasked with investigating a critical regression in our custom data ingestion service. The service recently started crashing, and we need you to perform a forensic analysis to identify the root cause, the exact commit that introduced the bug, and artifacts from the crash.

You have been provided with the following resources:
1. `/home/user/repo`: A local Git repository containing the source code for the service. The repository has exactly 200 commits. The file of interest is `processor.py`, which contains a `deserialize(payload: bytes)` function.
2. `/home/user/traffic.pcap`: A network packet capture containing the traffic sent to the service right before it crashed. The service listens on TCP port 8888. One of the packets sent to this port contains the exact malicious payload that triggers the crash. The payload always starts with the bytes `DATA:`.
3. `/home/user/crash.dmp`: A raw memory dump of the python process taken immediately after a previous crash. Due to an encoding mishandling, a specific corrupted string artifact is left in memory. It is a string formatted exactly like `ERR_STATE_{HEX_STRING}`.

Your objectives are:
1. **Pcap Analysis**: Extract the raw bytes of the crashing payload (starting with `DATA:`) sent to TCP port 8888 from `/home/user/traffic.pcap`.
2. **Memory Dump Analysis**: Analyze `/home/user/crash.dmp` to extract the `ERR_STATE_{HEX_STRING}` string.
3. **MRE Creation**: Write a minimal reproducible example (MRE) script at `/home/user/mre.py`. This script must import `deserialize` from `processor.py` and pass the extracted raw payload to it. The script should exit with code 1 if the function raises an exception (indicating the bug is present) and exit with code 0 if it succeeds.
4. **Bisection**: Use your `mre.py` script to automate a `git bisect` on `/home/user/repo` to find the exact commit hash that introduced the regression. The commit `HEAD` is known to be bad, and the oldest commit (the very first commit in the repository) is known to be good.

Once you have completed the analysis, output your findings to a JSON file at `/home/user/report.json` with the following exact schema:
```json
{
  "crashing_payload_hex": "<the extracted payload as a hex string, e.g., '444154413a...'>",
  "error_state_string": "<the exact ERR_STATE_... string found in the dump>",
  "bad_commit_hash": "<the full 40-character SHA-1 hash of the first bad commit>"
}
```