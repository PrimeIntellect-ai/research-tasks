We have a critical support ticket from a customer using our network inspection appliance. They provided a diagnostic packet capture (`/app/diagnostic_capture.pcap`) that causes our custom Python parsing library, `custom_net_parser`, to crash with an unhandled exception. 

The appliance uses a Python package called `custom_net_parser` (vendored at `/app/custom_net_parser`) to extract metadata from a proprietary telemetry protocol (Protocol ID: 0x88). 

Your task as a support engineer is to:
1. Analyze the `/app/diagnostic_capture.pcap` file and reproduce the crash using the vendored `custom_net_parser` package. You may want to use `pdb` or another Python interactive debugger to isolate exactly where and why the parser fails on the malformed or edge-case packet in the capture.
2. Identify the root cause of the bug in the `/app/custom_net_parser` source code and fix it in place. The bug is related to how payload lengths are calculated for packets with a specific flag, similar to an out-of-bounds read or buffer overflow concept in C, but manifesting here as a Python slicing/unpacking error.
3. Write a regression test suite in `/home/user/test_regression.py` that reads the pcap and asserts that the parser successfully processes all packets without crashing.
4. Create an integration script at `/home/user/parse_runner.py` that takes a single command-line argument containing a raw hex-encoded packet payload (e.g., `python3 /home/user/parse_runner.py 0800fa...`), processes it using your patched `custom_net_parser.parse()` function, and prints the resulting Python dictionary as a valid JSON string to `stdout`.

To ensure your fix is correct, we have provided an older, stripped, compiled C reference implementation (the oracle) at `/app/oracle_parser`. Your Python integration script (`/home/user/parse_runner.py`) must produce BIT-EXACT JSON output identical to the oracle when given the same hex-encoded payload. Our automated verifier will aggressively fuzz your script against this oracle using thousands of randomly generated packet inputs.

Constraints:
- You must fix the vendored package directly in `/app/custom_net_parser`.
- Output of `/home/user/parse_runner.py <hex_string>` must perfectly match the output of `/app/oracle_parser <hex_string>`.
- Only use standard Python library modules (like `json`, `struct`, `pdb`) and the provided vendored package for your script. Do not install external libraries to bypass the vendored parser.