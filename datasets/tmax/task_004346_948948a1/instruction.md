You are a security researcher analyzing a suspicious binary's custom command-and-control (C2) protocol. The C2 communicates over custom UDP packets. We have captured several interactions and placed them in pcap files. 

We are using a third-party, multi-language parsing package to extract telemetry data from these packets. However, the parser seems to be malfunctioning. Legitimate telemetry data is being misidentified, and malicious data is slipping through. Upon initial investigation, the issue appears to be related to how the parser handles 64-bit coordinate telemetry, potentially suffering from precision loss when translating between the C backend and the Python frontend.

Your task has two parts:
1. Inspect and fix the vendored parsing package located at `/app/vendored_parser`. There is a deliberate bug causing precision loss when extracting the `latitude` and `longitude` fields from the custom packets. You must fix the code and recompile/reinstall the package in the local environment so that 64-bit floating-point precision is preserved.
2. Create a classification script at `/home/user/classifier.py` that takes a directory of pcap files as a command-line argument. The script must parse each pcap using the fixed `/app/vendored_parser` library.
   - For each packet parsed, calculate the Euclidean distance from the coordinates `(0.0, 0.0)`.
   - If the distance is exactly `1337.0000000000000` (requiring full 64-bit precision to verify), the packet is malicious.
   - The script must print the classification for each file to standard output in the exact format: `[FILENAME]: EVIL` or `[FILENAME]: CLEAN`. If any packet in the pcap is malicious, the whole file is EVIL.

Requirements:
- Ensure you fix the C-extension and rebuild it (a `Makefile` is provided in `/app/vendored_parser`).
- The script must accept a single argument: the path to the directory containing `.pcap` files.
- The script must correctly classify all files without dropping precision.