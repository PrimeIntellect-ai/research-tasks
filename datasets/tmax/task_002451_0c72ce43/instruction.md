You are a support engineer investigating a script failure. The Python script `/home/user/parse_pcap.py` is designed to read custom UDP sensor telemetry from a network capture `/home/user/traffic.pcap` and print the parsed records.

However, the script is currently crashing with a traceback when run against the provided pcap file due to an edge case in the custom protocol format. 

Your tasks:
1. Analyze the traceback and inspect the pcap file to understand the crash.
2. Fix the Python script so that it gracefully handles the malformed packet. Specifically, if a message of Type 2 specifies a length that exceeds the available remaining payload bytes, the script should print `Malformed packet: length X exceeds payload` (where X is the parsed length value from the packet) and skip to the next packet.
3. Run the fixed script on `/home/user/traffic.pcap` and redirect its standard output to `/home/user/parsed_data.log`.

Constraints:
- Do not modify the input file `/home/user/traffic.pcap`.
- The fixed script must be able to process the rest of the valid packets after a malformed one.