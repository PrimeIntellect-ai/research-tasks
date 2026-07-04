You are tasked with debugging and fixing a failing multi-service network packet inspection pipeline.

The system consists of three components located in `/home/user/app/`:
1. **Traffic Emitter (`/home/user/app/emitter/`)**: A Python service that streams a pre-captured network trace (`traffic.pcap`) over a raw TCP socket on port 9000.
2. **Aggregator (`/home/user/app/aggregator/`)**: A Python Flask service listening on port 8080. It receives JSON payloads containing parsed packet metrics and appends them to `/home/user/app/aggregator/parsed_tlvs.log`.
3. **DPI Daemon (`/home/user/app/daemon/`)**: A C program that connects to port 9000, reads the raw packet stream, parses nested TLV (Type-Length-Value) structures from the payloads, and posts the results to the Aggregator on port 8080.

Currently, the system is broken in two ways:
**Phase 1: Build Failure & Dependency Conflict**
Navigate to `/home/user/app/daemon/` and run `make`. The build fails due to a dependency conflict. The project was recently refactored to use the system's `libpcap` instead of a legacy local mock (`libpcap-mock.so` in `../lib/`). However, the `Makefile` and include directives are still pulling in conflicting headers or libraries, causing compilation and linking errors. Resolve these conflicts so the daemon compiles successfully.

**Phase 2: Infinite Loop & Integer Overflow**
Once built, start the services. You will find that the DPI Daemon processes a few packets and then suddenly hangs (consuming 100% CPU) or crashes.
The issue is inside `parser.c`, specifically in the recursive TLV parsing logic. A malicious packet in `traffic.pcap` contains a crafted payload that triggers a signed integer overflow. This bypasses the validation checks, leading to an infinite loop or bad recursion.
- Analyze `traffic.pcap` using standard tools if necessary to understand the payload.
- Add `assert()` statements in `parser.c` to validate intermediate length calculations and trap the overflow.
- Fix the logic in `parser.c` so that it correctly handles the invalid lengths (e.g., by returning an error gracefully) without hanging or crashing.

**Phase 3: Integration and Verification**
Run the full pipeline:
1. Start the Aggregator: `python3 /home/user/app/aggregator/server.py &`
2. Start the Emitter: `python3 /home/user/app/emitter/stream.py /home/user/app/traffic.pcap &`
3. Run your fixed daemon: `/home/user/app/daemon/dpi_daemon &`

Your goal is for the DPI daemon to successfully process the entire pcap stream without hanging. 
To succeed, the total number of successfully parsed and logged TLVs (lines in `/home/user/app/aggregator/parsed_tlvs.log`) must exceed a specific threshold (the full clean packet count) within a 5-second run.