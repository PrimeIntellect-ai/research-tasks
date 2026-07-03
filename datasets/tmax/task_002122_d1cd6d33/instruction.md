Wake up, it's 3 AM and you are on-call. Our backend `MathEngine` service just locked up and stopped responding to requests. 

The service listens for UDP packets on port 8888, extracting a JSON payload and computing a mathematical sequence (the Collatz conjecture sequence). We suspect a "poison pill" payload caused an infinite loop in the recursive/iterative logic, maxing out the CPU.

Here is what you need to do to resolve this incident:

1. **Analyze the Network Capture**: We have a packet capture of the traffic leading up to the failure located at `/home/user/traffic.pcap`. You will need to extract the JSON payloads from the UDP packets destined for port 8888. Identify the last integer `value` received before the service locked up.
2. **Fix the Loop Termination**: The service source code is at `/home/user/math_service.py`. Locate the `compute_collatz(n)` function. It contains a loop termination bug when handling certain invalid or edge-case integers (like the one you found in the pcap). Modify the function so that if it receives any integer `n <= 0`, it immediately returns an empty list `[]` instead of entering an infinite loop.
3. **Run Assertion Validations**: We have an intermediate validation script at `/home/user/validate.py`. It runs assertion-based validation against `math_service.py`. You must run this script and ensure it exits with code 0 (no assertion errors).
4. **Create the Incident Report**: Write a summary report to `/home/user/incident_report.txt` containing exactly two lines:
   - Line 1: The exact integer value from the packet capture that caused the infinite loop.
   - Line 2: The word `SUCCESS` (to confirm validation passed).

You have root access via `sudo` to install any necessary tools (like `tcpdump`, `tshark`, or python packages like `scapy`) to analyze the `.pcap` file. Ensure your final report strictly matches the requested format.