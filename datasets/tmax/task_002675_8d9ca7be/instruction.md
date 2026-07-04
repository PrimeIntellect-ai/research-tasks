You are tasked with investigating a critical failure in a long-running Python data processing service located in `/home/user/sensor_service`. The service relies on a custom C extension to process high-frequency sensor payloads quickly. 

Recently, the service has been experiencing two major issues:
1. It crashes abruptly (segmentation fault) when processing specific "large batch" sensor events.
2. Even when it doesn't crash, the container eventually OOMs (Out of Memory) after running for a few hours, indicating a memory leak.

Additionally, a junior developer recently touched the `Makefile` and now the C library won't even compile on our x86 Linux system.

Your objectives are:
1. **Fix the Build Misconfiguration:** Repair the `Makefile` in `/home/user/sensor_service` so that `make` successfully builds the shared library `libsensor.so`.
2. **Diagnose and Fix the Crash:** The crash happens when the service receives a large payload (e.g., 50,000 packets of 50,000 bytes each). Use debugging tools to analyze the failure. There is a signed integer overflow happening in `sensor_lib.c` that causes an invalid memory allocation size. Fix the C code to use `size_t` where appropriate to prevent this overflow and crash.
3. **Fix the Memory Leak:** Identify and fix the memory leak. The C library allocates a buffer for processing, but this memory is never freed. Modify `sensor_lib.c` to expose a `free_buffer` function if necessary, and update `service.py` to call it, OR fix the leak directly inside the C function if the buffer isn't needed after the function returns.
4. **Create a Regression Test:** Write a Python test script named `/home/user/sensor_service/test_regression.py`. This script must:
    - Load the fixed `libsensor.so`.
    - Call the processing function with `packet_count = 60000` and `packet_size = 50000` to verify the overflow crash is fixed.
    - Run a loop of 10,000 iterations calling the processing function with `packet_count = 100`, `packet_size = 1024`.
    - Monitor its own memory usage (using the `psutil` or `resource` module). The memory usage must not grow by more than 10MB during the 10,000 iterations.
    - If all tests pass, the script must write the exact string "REGRESSION_TEST_PASSED" to `/home/user/sensor_service/regression_result.log`.

Recompile the library and ensure your `test_regression.py` runs successfully and produces the expected log file.