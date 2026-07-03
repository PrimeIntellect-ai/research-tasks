You are a systems engineer investigating a memory leak in a long-running data ingestion service. You have been provided with a partially complete source tree for the service, which relies on a pre-compiled, closed-source shared library (`libprocessor.so`).

Currently, the service refuses to build due to linker errors. Your objectives are to resolve the build failures, create a minimal reproducible example (MRE) to isolate the leak, and quantify the memory leak.

The relevant files are located in `/home/user/service/`:
1. `/home/user/service/processor.h` - The header file for the shared library (suspected to have an inaccurate declaration).
2. `/home/user/service/libprocessor.so` - The pre-compiled shared library containing the data processing logic.
3. `/home/user/service/service.cpp` - A basic main runner that attempts to use the library.

**Your tasks:**
1. Interpret the compiler/linker errors when trying to build `service.cpp` with `libprocessor.so`.
2. Inspect the compiled binary `libprocessor.so` to determine the correct function signature and fix `processor.h` and `service.cpp` so they compile and link successfully. (Command to link: `g++ service.cpp -o service -L. -lprocessor -Wl,-rpath=.`)
3. Debug the resulting binary to determine the exact number of bytes leaked in memory *per single call* to the data processing function.

**Output:**
Create a report at `/home/user/debug_report.txt` with exactly two lines:
* **Line 1:** The exact demangled C++ signature of the target function found in the shared library (e.g., `void calculate_metrics(float const*, int)`).
* **Line 2:** The exact number of bytes leaked by a single execution of that function (e.g., `256`).

Do not include any other text, markdown formatting, or explanations in `/home/user/debug_report.txt`.