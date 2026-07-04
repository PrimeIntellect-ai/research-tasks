You have inherited an unfamiliar C++ codebase that processes binary telemetry data. Recently, the service has started crashing with segmentation faults when encountering certain edge-case serialized data. 

The codebase and a sample malformed input file are located in `/home/user/telemetry_service`.

Your task is to:
1. Debug the segmentation fault occurring when the program processes `/home/user/telemetry_service/input.bin`.
2. Identify the exact `double` value that is being read into the `sensor_val` field of the `Packet` struct right before the out-of-bounds access.
3. Write this precise `double` value (e.g., `4.5`, `-1.5`, etc.) into a text file at `/home/user/crash_value.txt`.
4. Fix the C++ code in `main.cpp` to prevent the crash. The system should safely ignore out-of-bounds indices instead of crashing. Ensure you account for precision loss and negative values correctly.
5. Compile your fixed code into an executable named `/home/user/telemetry_service/telemetry`. 
6. Ensure that running `/home/user/telemetry_service/telemetry /home/user/telemetry_service/input.bin` exits gracefully with exit code 0.

You may use standard Linux debugging tools like `gdb` to trace the fault.