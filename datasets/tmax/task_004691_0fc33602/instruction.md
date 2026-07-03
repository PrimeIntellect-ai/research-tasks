You are a performance engineer tasked with profiling and debugging a custom audio processing application.

We have a C++ application that processes audio transmissions, computing a rolling RMS energy and then performing a custom delta encoding. However, the application has two major issues:
1. It crashes (Segmentation Fault) when processing certain edge-case data in the provided audio file.
2. It is extremely slow due to an unoptimized mathematical bottleneck in the energy computation phase.

Files provided in the environment:
- `/app/processor.cpp`: The source code of the application.
- `/app/transmission.wav`: The audio fixture containing the transmission data.

Your objectives:
1. **Memory / Crash Analysis**: Compile and run `/app/processor.cpp`. It will crash and dump core (ensure you set `ulimit -c unlimited`). The application generates a unique 16-character Session ID during initialization which is stored in memory but NOT printed. Extract this Session ID from the core dump (or by analyzing the memory state at the crash point) and save it exactly to `/app/session_id.txt`.
2. **Delta Debugging & Bug Fixing**: Identify why the application crashes during the delta serialization phase on this specific audio file. Fix the bug in `/app/processor.cpp` so that it successfully processes the entire file without altering the intended encoding logic for valid samples.
3. **Performance Optimization**: The `compute_rolling_energy` function is mathematically correct but algorithmically inefficient (O(N * W)). Refactor this function to be O(N) using a rolling sum/mathematical recurrence approach. The optimized version must produce mathematically identical floating-point results (within standard IEEE 754 precision) but run significantly faster.
4. **Final Output**: Save your fixed and optimized source code as `/app/processor_fixed.cpp`. Compile it to an executable named `/app/processor_fixed`. Run it on `/app/transmission.wav` to produce `/app/output.bin`.

The automated verifier will measure the execution time of `/app/processor_fixed /app/transmission.wav /app/output.bin`. To pass, the application must yield the correct output bytes and the execution time must strictly meet the performance threshold (under 0.1 seconds).