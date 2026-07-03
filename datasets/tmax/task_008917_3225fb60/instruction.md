You are a Site Reliability Engineer (SRE) investigating a recent outage of a critical C++ microservice, `metrics_processor`. The service listens for UDP metric packets on port 8080 but has been intermittently crashing.

You have been provided with the following files in `/home/user/`:
1. `metrics_processor.cpp`: The source code of the currently deployed (and crashing) service.
2. `logs/uptime_monitor.log`: The system log showing service status and the exact time it went down.
3. `capture.pcap`: A network packet capture containing the traffic sent to port 8080 leading up to the crash.

Your task is to reconstruct the timeline of the crash, identify the malicious or malformed packet that caused it, find the root cause in the C++ code, and write a fix.

Specifically, you must:
1. Correlate the crash timestamp in the log file with the packets in the pcap file to find the exact UDP packet sent immediately before the crash.
2. The custom UDP protocol specifies that the first 4 bytes of the payload represent a little-endian `Sequence ID` (uint32_t). Extract the Sequence ID of the packet that caused the crash.
3. Analyze `metrics_processor.cpp` to understand why this specific packet payload caused a crash (e.g., intermediate state corruption, buffer overflow).
4. Create a corrected version of the source code at `/home/user/metrics_processor_fixed.cpp`. This file must successfully compile (`g++ -std=c++17 -o fixed metrics_processor_fixed.cpp`) and fix the bug without removing existing functionality.
5. Create a JSON report file at `/home/user/root_cause.json` containing your findings. It MUST have exactly the following structure and keys:
```json
{
  "crash_timestamp": "YYYY-MM-DD HH:MM:SS",
  "crashing_seq_id": 123,
  "buggy_function": "name_of_the_c++_function_with_the_bug"
}
```
*Note: Ensure your fixed code retains the original file's includes and structure.*