You are a support engineer investigating a server crash. A customer reported that their C-based UDP server crashes when receiving a specific network packet. They have provided the server's source code and a packet capture of the traffic leading up to the crash.

You have been given the following files in `/home/user/`:
- `server_src/`: A directory containing the C source code (`server.c`) and a `Makefile`.
- `crash.pcap`: A network packet capture containing the packet that caused the crash.

Your tasks:
1. **Fix the build**: The provided `Makefile` is incomplete and currently fails to build the `server` binary due to a linker error. Diagnose the missing library dependency, modify the `Makefile` to fix it, and build the server.
2. **Analyze the PCAP**: Inspect `crash.pcap` to extract the exact UDP payload sent to the server on port 9000.
3. **Diagnose the crash**: Reproduce the crash by sending the extracted payload to the built server. Use a debugging tool (like `gdb` or `valgrind`) to analyze the crash and determine the exact C function where the segmentation fault (buffer overflow) occurs.
4. **Report**: Create a report file at `/home/user/report.txt` containing exactly three lines:
   - Line 1: The exact flag you added to the Makefile to fix the linker error (e.g., `-lpthread`).
   - Line 2: The exact string payload extracted from the PCAP file.
   - Line 3: The exact name of the C function where the segmentation fault occurs.

Ensure your report is formatted exactly as requested, with no extra text or empty lines.