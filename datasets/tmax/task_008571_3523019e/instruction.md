You are an engineer investigating a severe memory leak in a long-running Python-based network analysis service. The service parses PCAP files to track stateful session data, but it crashes with Out-Of-Memory (OOM) errors when processing certain network traffic.

You have been provided with:
1. The buggy script: `/home/user/network_parser.py`
2. A packet capture file that triggers the leak: `/home/user/capture.pcap`

Your objectives are:
1. **Root Cause Analysis via Delta Debugging**: The `capture.pcap` file contains many packets, but only one specific packet triggers the memory leak state. You must use delta debugging/test minimization techniques (e.g., bisection) to isolate the exact packet that causes the unbounded memory growth.
2. Identify the **1-indexed packet number** (e.g., if it's the 5th packet in the file, the answer is 5) of the offending packet in the original `capture.pcap` file. Write this single integer to `/home/user/leak_packet.txt`.
3. **Fix the Bug**: Read and comprehend `/home/user/network_parser.py`. Identify the logic flaw causing the leak when this specific packet is processed. 
4. Save the corrected script as `/home/user/network_parser_fixed.py`. The fixed script must retain all normal session tracking functionality but prevent the memory leak when processing the malformed/trigger packet.

Constraints:
- You must use standard Python or Bash tools. `scapy` is available for PCAP manipulation and reading.
- Do not modify the original `capture.pcap` file.
- The fixed script must output `Leaked buffer items: 0` when run on `capture.pcap`.