You are a support engineer investigating a mathematical processing pipeline that keeps intermittently failing. 

The client has provided a network capture of the internal API traffic (`/app/traffic.pcap`) and a screenshot of the original mathematical specification (`/app/spec.png`). 

The current validation script (`/app/legacy_validator.py`) intermittently crashes in production, similar to how poorly written shell scripts break on filenames with spaces. It struggles with specific payload encodings and edge cases found in the queries.

Your task is to:
1. Extract the mathematical constraints and required variable names from the image (`/app/spec.png`).
2. Analyze the network packet capture (`/app/traffic.pcap`) to understand the structure of the incoming JSON payloads that the API expects.
3. Fix the environment/dependencies if needed to parse the pcap (the client mentioned `scapy` might be missing or misconfigured in the default Python environment).
4. Debug why the legacy validator fails on edge-case queries (delta debugging the failures).
5. Write a robust Python classifier script at `/home/user/sanitizer.py`.

The `sanitizer.py` script must take exactly one argument: the absolute path to a JSON file containing a payload.
- It MUST exit with code `0` if the payload perfectly satisfies the mathematical constraints and structure derived from the image and pcap (a "clean" payload).
- It MUST exit with code `1` if the payload violates the mathematical constraints, contains malformed data, triggers the zero-division edge cases, or has malicious type injections (an "evil" payload).
- It MUST NOT crash under any input circumstances (e.g., unexpected strings, spaces, or missing keys).

To verify your solution, the automated test will run your `/home/user/sanitizer.py` against two provided corpora:
- `/app/corpus/clean/` : Directory containing exclusively valid JSON payloads.
- `/app/corpus/evil/` : Directory containing payloads that violate constraints or contain malicious edge cases.

You are expected to accurately preserve all clean payloads and reject all evil payloads.