You have recently been assigned to maintain a legacy Python project located at `/home/user/legacy_telemetry`. This codebase processes custom UDP telemetry packets from IoT sensors. However, the pipeline is currently broken, and the previous developer left without handing it over properly. 

Your objective is to fully restore and debug the pipeline to produce the correct analytical results.

Here is what you need to do:

1. **Recover the Missing Data**:
   The test data file, `sample.pcap`, is missing from the `data/` directory. The previous developer committed it to the git repository at some point but subsequently deleted it in a later commit to "save space." You must find and restore `sample.pcap` from the git history and place it exactly at `/home/user/legacy_telemetry/data/sample.pcap`.

2. **Fix the Parsing Bug**:
   The parsing logic in `reader.py` uses the `dpkt` library to read the pcap file and extract custom UDP payloads. The payload format is supposed to be:
   - Bytes 0-3: Sensor ID (32-bit unsigned integer, big-endian)
   - Bytes 4-11: Measurement Value (64-bit float, big-endian)
   - Bytes 12+: Sensor Name (UTF-8 string)
   However, `reader.py` crashes on a specific edge case in the network capture. Identify the format parsing edge case and modify `reader.py` so that it successfully parses all packets. If a packet's Sensor Name is empty, it should be parsed as an empty string `""`.

3. **Repair Floating-Point Precision**:
   Once the parser is fixed, `main.py` will pass the extracted measurement values to `analytics.py` to compute the sample variance of the measurements. The current implementation in `analytics.py` uses a naive formula (`E[X^2] - (E[X])^2`) which suffers from catastrophic cancellation due to floating-point precision issues (the measurements are very close to a large base value, e.g., 100000000.0). Fix `analytics.py` so that it computes the sample variance accurately without losing precision. 

4. **Generate the Output**:
   Once you have recovered the file and fixed the bugs, run the pipeline:
   `python main.py`
   This will automatically generate a file at `/home/user/legacy_telemetry/result.txt` containing the final variance. 

**Constraints & Notes**:
- You must use Python 3.
- You can install any standard packages using `pip` (e.g., `dpkt`), but the core logic fixes must be written by you.
- Do not hardcode the final answer; your code must dynamically process `sample.pcap`.
- Do not change the file path or name of `/home/user/legacy_telemetry/result.txt`.