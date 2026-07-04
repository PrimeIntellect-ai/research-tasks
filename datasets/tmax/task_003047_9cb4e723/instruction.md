You are an engineer investigating a recurring crash and a memory leak in a long-running data processing service.

The service reads base64-encoded payloads from standard input (one per line), decodes them, and prints the result to standard output. Under high load with potentially malformed inputs, the service leaks memory and eventually crashes. 

We have captured a recent crash. You will find:
- A core dump at `/home/user/crash/core`
- The last logs before the crash at `/home/user/crash/service.log`

The service's source code and its vendored base64 parsing package are located in `/app/`. The project uses a vendored version of the popular `cpp-base64` library located at `/app/cpp-base64`.

Your tasks:
1. Analyze the core dump and logs to identify the exact cause of the crash. You will find an off-by-one boundary condition in the vendored base64 library (`/app/cpp-base64/base64.cpp`) that triggers an out-of-bounds read when processing certain inputs.
2. Fix the boundary condition bug in the vendored library.
3. Identify and fix a memory leak in the wrapper program `/app/service_worker.cpp` that occurs when processing invalid inputs.
4. Compile your fixed version. You must use the provided `/app/Makefile`.
5. Copy the final fixed executable to `/home/user/fixed_worker`.

Your fixed binary will be strictly verified against a reference oracle. It must not crash on malformed inputs, must not leak memory, and its standard output must be bit-for-bit identical to the expected decoding behavior for thousands of randomized fuzz inputs.

Constraints:
- Do not modify the expected input/output format of the service.
- The compiled binary must be placed exactly at `/home/user/fixed_worker`.