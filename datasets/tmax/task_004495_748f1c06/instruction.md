You are a performance engineer tasked with debugging and fixing our real-time data processing stack. The system consists of an Nginx reverse proxy and a custom C++ backend service. Currently, the system is inoperable due to several critical bugs.

Your tasks are:

1. **Database Recovery**: The C++ backend reads a custom binary WAL (Write-Ahead Log) on startup located at `/app/data/journal.bin`. This file was corrupted during a crash. A valid record consists of:
   - A 4-byte magic number: `0xDEADBEEF` (little-endian)
   - An 8-byte IEEE 754 double-precision float (little-endian)
   - A 4-byte checksum, which is calculated as the bitwise XOR of the two 4-byte halves of the 8-byte float (i.e., `(uint32_t)half1 ^ (uint32_t)half2`).
   Write a C++ program to parse `/app/data/journal.bin`, recover all sequentially valid floating-point numbers up to the first corrupted byte, and output them to `/app/data/recovered.csv`, one float per line, formatted to 6 decimal places.

2. **Numerical Instability & Concurrency Debugging**: The C++ backend source code is located in `/app/src/backend.cpp`. 
   - It computes the variance of a list of floats sent via HTTP POST to the `/compute` endpoint. It currently suffers from numerical instability: arrays with massive baseline values (e.g., `[1e16, 1e16+1, 1e16+2]`) cause catastrophic cancellation or NaNs, triggering an infinite `while` loop in the mathematical optimization routine. 
   - Furthermore, the HTTP server leaks a worker thread if a client drops the TCP connection prematurely during a chunked upload. You must use container/log inspection and profiling to identify the exact lines causing these issues and fix them.

3. **Regression & Fuzz Testing**: Create a libFuzzer target in `/app/src/fuzz_test.cpp` that links against the variance computation function in `backend.cpp`. The fuzzer must accept arbitrary byte arrays, interpret them as vectors of `double`, and pass them to the computation function to prove that the infinite loop is fixed.

4. **Integration**: Modify `/app/src/Makefile` to build both the backend and the fuzzer. Compile the backend and run `/app/start.sh` to bring up the multi-service compose stack. 

The final system must have Nginx listening on TCP port `8080`, proxying requests to the C++ backend on port `8081`. 

Ensure that:
- `/app/data/recovered.csv` contains the correctly recovered data.
- The C++ backend does not hang on numerically unstable inputs.
- The C++ backend does not leak threads upon client disconnects.
- Nginx and the backend are both running properly.