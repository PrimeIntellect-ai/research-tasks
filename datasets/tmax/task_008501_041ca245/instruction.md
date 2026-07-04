**PAGE ALERT - 03:15 AM - SEVERITY: HIGH**

You are the on-call engineer. Our high-frequency telemetry ingestor has failed. The application is supposed to parse offline network packet captures (.pcap) containing raw UDP sensor data, apply a simple transformation, and write the normalized data to disk. 

However, two critical issues are occurring:
1. **Silent Failure:** The ingestor process is terminating immediately without writing any data. The logs are empty. You will need to trace its system calls to figure out why it is aborting.
2. **Data Corruption / Precision Loss:** Yesterday, before the pipeline fully broke, downstream financial models triggered alarms about data transformation diffs. They suspect precision loss during the payload extraction phase. 

**System Details:**
- **Source Code:** `/home/user/telemetry_ingest.cpp`
- **Input Data:** `/home/user/traffic.pcap`
- **Network Payload Specification:** Inside the UDP payload, the data is structured exactly as: `[4 bytes Sensor ID (uint32, big-endian)] [8 bytes Sensor Value (IEEE 754 double precision, big-endian)]`.
- **Expected Output:** The program must write the extracted data to `/home/user/data.out` in the exact format: `Sensor <ID>: <Value>\n` (Value formatted with exactly 6 decimal places, e.g., `%.6f`).

**Your Tasks:**
1. Diagnose and fix the system call failure that causes the immediate exit. (Hint: trace the process).
2. Fix the precision loss bug in `/home/user/telemetry_ingest.cpp`. 
3. Recompile the program: `g++ -o /home/user/telemetry_ingest /home/user/telemetry_ingest.cpp -lpcap`
4. Run the compiled program so it successfully processes `/home/user/traffic.pcap` and generates the perfectly accurate `/home/user/data.out`.

When you are finished, the file `/home/user/data.out` must exist and contain the correct, high-precision values parsed from the pcap without any loss.