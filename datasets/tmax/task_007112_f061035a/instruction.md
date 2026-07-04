You have recently inherited a legacy C++ codebase for a telemetry aggregator daemon. The previous developer left abruptly, and the operations team is reporting that the daemon sporadically crashes when processing certain daily log files. 

Your environment has been set up with the codebase in `/home/user/telemetry`. 

Inside this directory, you will find:
1. `telemetry_processor.cpp` - The C++ source code that reads a custom binary encoding format and calculates aggregate statistics.
2. `Makefile` - For building the `telemetry_processor` binary.
3. `generate_traffic.py` - A python script that simulates the incoming telemetry stream and generates a `data.bin` file.

**The Problem:**
Running `./telemetry_processor data.bin` results in a segmentation fault or unhandled exception somewhere deep in the processing loop. Preliminary statistical anomaly investigation suggests the crash happens due to intermittent edge-case data in the custom VarInt encoding sequence that corrupts memory or causes out-of-bounds reads.

**Your Objectives:**
1. Generate the test dataset by running `python3 generate_traffic.py`. This will create `/home/user/telemetry/data.bin`.
2. Debug `telemetry_processor.cpp` to identify the root cause of the crash (analyze the custom serialization/varint decoding diffs).
3. Fix the C++ code so that it handles out-of-bounds buffer access gracefully during VarInt decoding. If the decoder encounters a truncated or malformed varint that attempts to read past the end of the provided buffer, it should throw a `std::runtime_error` with the exact message `"Buffer overflow during varint decoding"`. The main processing loop is already set up to catch `std::runtime_error` and print the final computed statistics before exiting.
4. Compile your fixed code using `make`.
5. Run your fixed `./telemetry_processor data.bin`.
6. Write the final exact output value of the "Total Sum" (which is printed to standard output upon successful completion or graceful error catch) into a file named `/home/user/solution.txt`.

Ensure your C++ fix strictly addresses the missing bounds checking in the `parse_varint` function without altering the core mathematical logic.