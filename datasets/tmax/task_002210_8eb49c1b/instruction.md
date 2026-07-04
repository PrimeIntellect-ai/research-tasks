You are a performance engineer tasked with debugging and profiling a high-throughput sensor data processing pipeline. 

Your team relies on a custom Python C-extension, `fast_sensor_calc`, to compute rolling statistics over network data. However, the system is currently broken on multiple fronts: the package fails to build, and when historically built, it exhibited severe numerical instability on our production data.

Your tasks are:

1. **Fix the Vendored Package Build:** 
   The source for the extension is located at `/app/vendored/fast_sensor_calc-0.1.0`. Currently, running `pip install -e .` fails with a linker/compiler error. Diagnose and fix the build configuration so the package installs successfully.

2. **Network Payload Extraction:**
   You are provided with a packet capture file at `/app/data/sensor_stream.pcap`. 
   - Filter for UDP traffic on port 5000.
   - The UDP payload of each packet consists of a sequence of 8-byte IEEE 754 double-precision floats (little-endian). 
   - Parse these packets in order. Each packet represents a single "window" of sensor readings.

3. **Diagnose and Fix Numerical Instability:**
   The `fast_sensor_calc` module has a function `compute_window_variance(List[float]) -> float`. 
   The current C implementation suffers from catastrophic cancellation (numerical instability) when processing the high-magnitude, low-variance data found in the pcap. 
   - Fuzz test or analyze the C code to identify the flaw in the mathematical algorithm.
   - Rewrite the variance calculation in the C-extension to be numerically stable (e.g., using Welford's algorithm or a two-pass mean approach) while maintaining high performance. 
   - Recompile the package.

4. **Integration and Profiling:**
   Write a Python script `/home/user/run_analysis.py` that:
   - Reads the pcap file and extracts the float arrays.
   - Passes each array to the corrected `fast_sensor_calc.compute_window_variance`.
   - Writes the resulting variances to `/home/user/output_variances.txt`, with one float per line (in the exact order the packets appear in the pcap).

Constraints:
- You must use the C-extension to perform the variance calculation. The automated verification will fail if the script is too slow (it must process the data faster than a pure Python implementation).
- Do not use external pcap-parsing tools like `tshark` to dump the data; parse the pcap within your Python script using standard libraries or `scapy`/`dpkt`.