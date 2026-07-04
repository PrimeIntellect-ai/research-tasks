You are tasked with debugging a failing Continuous Integration (CI) build for a distributed mathematical simulation engine. The test suite fails intermittently during the integration phase, reporting a numerical instability (`ZeroDivisionError` or `OverflowError`). 

The build directory is located at `/home/user/simulation_build/`.

You have been provided with the following:
1. `/home/user/simulation_build/math_engine.py`: The core computation module containing the `compute_trajectory(payload_dict)` function.
2. `/home/user/simulation_build/traffic_capture.pcap`: A packet capture file containing network traffic recorded during a failing test run.

Your objectives are:
1. **Analyze the PCAP**: Use a Python packet analysis library (like `scapy`, which you may need to install) to read `traffic_capture.pcap`. Extract the UDP payloads sent to port 9000. These payloads are JSON strings representing 3D coordinates: `{"x": float, "y": float, "z": float}`.
2. **Reproduce the Failure**: Write a script to feed these extracted payloads one-by-one into `math_engine.compute_trajectory()` to identify exactly which packet causes the numerical instability. 
3. **Fix the Bug**: The bug in `math_engine.py` is caused by a division by a value that can become exactly zero. Modify `math_engine.py` to prevent this by adding a small epsilon (`1e-9`) to the denominator before division.
4. **Report**: Create a JSON file at `/home/user/bug_report.json` with the following exact structure containing the details of the failure:
```json
{
  "problematic_packet_index": <int, 0-indexed position of the UDP packet to port 9000 that caused the crash>,
  "problematic_payload": {"x": <float>, "y": <float>, "z": <float>}
}
```

Ensure your modified `math_engine.py` no longer crashes when processing the problematic payload and returns a valid float.