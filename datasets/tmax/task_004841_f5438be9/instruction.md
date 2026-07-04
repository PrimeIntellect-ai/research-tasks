We have a legacy data-processing application located in `/app/legacy_proc` that is currently failing to start. It acts as a TCP microservice but is suffering from a shared library linking issue and missing configuration parameters. 

Your objective is to debug the ABI mismatch, recover the missing configuration from a scanned engineering memo, and write a Bash-based wrapper to serve the application robustly.

**System State & Requirements:**
1. **The Binary:** There is a compiled C binary at `/app/legacy_proc/bin/data_engine`. If you try to run it, it currently crashes with a segmentation fault or library linking error. 
2. **Library Conflict:** The binary depends on `libmatrix_math.so`. There are two conflicting versions installed in `/app/legacy_proc/lib/v1/` and `/app/legacy_proc/lib/v2/`. You must use tools like `ldd` and `strace` to determine which version satisfies the correct ABI for the binary, and set up your environment accordingly.
3. **The Scanned Memo:** There is an image file at `/app/legacy_proc/docs/handwritten_memo.png`. This image contains a handwritten note from the original author detailing a critical environment variable required to prevent memory corruption in the C library during high loads. You must read this image (using OCR like `tesseract` or other available tools) to extract the exact environment variable name and its hexadecimal value.
4. **The Bash Service Wrapper:** Write a Bash script at `/app/legacy_proc/start_service.sh`. This script must:
   - Setup the correct library path so the binary links successfully.
   - Export the exact environment variable recovered from the image.
   - Use `socat` (or `nc`) to bind the binary to a TCP port, creating a network service.
5. **Network Specifications:** The service must listen on port `9099` on all interfaces (`0.0.0.0`). It must accept incoming TCP connections. When a client sends a newline-terminated string, the `data_engine` binary processes it and returns the result. The Bash wrapper must spawn a new process for each connection (e.g., using `socat`'s `fork` option).
6. **Benchmarking:** Write a benchmarking script at `/app/legacy_proc/benchmark.sh` that sends 100 requests to `127.0.0.1:9099` and logs the total execution time to `/app/legacy_proc/bench_results.log`.

Do not modify the `data_engine` binary itself. Your solution must rely entirely on environment configuration, Bash scripting, and TCP wrapping.