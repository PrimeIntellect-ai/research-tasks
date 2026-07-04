You are a support engineer tasked with collecting diagnostics and patching a failing telemetry pipeline for an IoT deployment. The pipeline has been reporting physically impossible temperature values. 

Your workspace is located at `/home/user/telemetry_diag`.

You have been provided with the following files in your workspace:
1. `traffic.pcap`: A network packet capture containing incoming UDP telemetry data.
2. `legacy_decoder`: A compiled, stripped Linux ELF binary that the legacy system used to decode raw hexadecimal payloads into raw integer metric values.
3. `pipeline.py`: A Python script that is supposed to process these payloads but currently produces incorrect temperature readings due to a buggy formula.
4. `datasheet.txt`: A text file containing the sensor manufacturer's formula for converting decoded raw integers into Fahrenheit.

Perform the following tasks:

**Phase 1: Packet Capture Analysis**
Analyze `traffic.pcap`. Extract the UDP payloads for all packets destined for port `8888`. 
Write the extracted payloads as continuous uppercase hexadecimal strings (e.g., `A1B2C3D4`), one per line, into `/home/user/telemetry_diag/extracted_payloads.txt`. Maintain the chronological order of the packets.

**Phase 2: Binary Reverse Engineering & Implementation**
The system currently relies on the black-box `legacy_decoder` binary. Run it to see how it works: it takes a single hex string argument and outputs an integer (e.g., `./legacy_decoder A1B2C3D4`). 
Reverse engineer the simple mathematical/bitwise transformation the binary applies to the input hex string to produce the integer. 
You must completely replace the binary dependency. Implement the reversed logic as a pure Python function `decode_payload(hex_str: str) -> int` inside `/home/user/telemetry_diag/pipeline.py`.

**Phase 3: Formula Implementation Correction**
Read `datasheet.txt` to understand the correct formula for converting the raw decoded integer into a Fahrenheit temperature. 
The current function `calculate_temperature(raw_val: int) -> float` in `pipeline.py` has a flawed implementation of this formula. Correct it. The function must return a float rounded to exactly 2 decimal places.

**Phase 4: Regression Test Construction**
Write a pytest suite in `/home/user/telemetry_diag/test_pipeline.py`. 
It must import `decode_payload` and `calculate_temperature` from `pipeline.py` and contain at least 4 test cases testing various payload strings and their final expected temperature outputs to prevent future regressions.

You have successfully completed the task when:
- `extracted_payloads.txt` contains the correct hex payloads.
- `pipeline.py` contains the fully functional, fixed pure-Python implementation without calling the external binary.
- `test_pipeline.py` is present and passes when run with `pytest`.