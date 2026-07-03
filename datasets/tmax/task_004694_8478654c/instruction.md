You are an IT support technician responding to an escalated incident. A legacy internal processing service crashed overnight, and you need to investigate the artifacts left behind, resolve a scripting issue, and submit a final incident report.

You have been provided with the following files in `/home/user/incident/`:
1. `traffic.pcap`: A network packet capture from the time of the crash.
2. `core.dmp`: A raw memory dump of the crashed process.
3. `parser.py`: A Python utility script used to generate the final checksum for the report, which currently fails to run due to a bug and environment issues.

Perform the following steps:

**Step 1: Network Analysis**
Analyze `/home/user/incident/traffic.pcap`. Find the source IP address that sent a packet containing the exact string payload `"FATAL_POISON"`. 

**Step 2: Memory Analysis**
Analyze `/home/user/incident/core.dmp`. The crash dumped a specific authentication token into memory. Find the string that matches the format `TOKEN-<32 hexadecimal characters>`.

**Step 3: Script Debugging**
Run `/home/user/incident/parser.py`. You will notice two issues:
1. It fails with a `RecursionError`. Fix the `compute_checksum` function in the script so that it correctly terminates. It is intended to calculate the sum of all positive integers down to 0 (e.g., `compute_checksum(3)` should return `6`).
2. Once the recursion is fixed, the script may fail due to a dependency conflict with the `urllib3` library. The script explicitly requires `urllib3` version `1.26.15`. Downgrade/install the correct version in your environment so the script runs successfully.

**Step 4: Reporting**
Run the fixed `parser.py` script. It will print a final integer checksum.
Create a file at `/home/user/report.txt` with exactly the following format (replace the bracketed placeholders with your findings):

```
IP: [IP Address]
TOKEN: [32-hex-char Token]
CHECKSUM: [Output of parser.py]
```