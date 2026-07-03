You are a developer debugging a failing build for a data processing pipeline.

The project is located in `/home/user/packet_project`. It consists of a C program (`parser.c`) that parses network packet captures (pcap) to extract metadata, and a test suite in Bash.
Currently, when you run `make test`, the test script feeds `sample.pcap` to the compiled `parser` binary, but it crashes with a Segmentation fault.

Your tasks are:
1. **Analyze the Crash**: Determine where and why the `parser` binary is crashing when processing `sample.pcap`. You may use `gdb` to analyze the execution or any core dumps.
2. **Bash Fuzzer**: Write a Bash script at `/home/user/packet_project/fuzz.sh` that isolates packets from `sample.pcap` (e.g., using `tcpdump` or `editcap`) and feeds them one by one to `./parser` to programmatically identify the exact packet number that causes the crash. 
3. **Fix the Bug**: Modify `parser.c` to fix the vulnerability (prevent the buffer overflow/out-of-bounds access) without removing the core parsing logic.
4. **Pass the Build**: Ensure `make test` runs successfully with an exit code of 0.
5. **Generate a Report**: Create a file at `/home/user/report.txt` with exactly two lines:
   - Line 1: The packet number (1-indexed, as shown by standard `tcpdump` output) in `sample.pcap` that causes the crash.
   - Line 2: The exact name of the C function in `parser.c` where the segmentation fault originated.

Constraints:
- You must write the `fuzz.sh` fuzzer entirely in Bash and ensure it has executable permissions (`chmod +x fuzz.sh`).
- Do not modify the `Makefile` or `test.sh`.