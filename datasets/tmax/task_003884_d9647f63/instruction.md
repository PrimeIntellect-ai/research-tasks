You are a systems programmer tasked with fixing an IoT payload ingestion pipeline. The system consists of multiple cooperating services, but it is currently broken due to a C library linking issue and incomplete validation logic.

Here is the current state of the system in `/home/user/iot_pipeline/`:
- `start_services.sh`: A script that launches the system services.
- `nginx/nginx.conf`: Configuration for the frontend reverse proxy.
- `src/daemon.c`: A C-based TCP daemon that receives payloads from nginx, processes them, and logs to a statistics service.
- `src/payload_filter.c`: The source code for `libpayload.so`, a dynamic library used by the daemon to validate incoming binary payloads.
- `src/Makefile`: The build script.

You have three primary objectives to get the pipeline fully operational:

1. **Fix the Linking Issue:** 
When you run `./start_services.sh`, the C daemon fails to start due to a dynamic linking error. Inspect `src/Makefile` and the compilation process. The daemon must be compiled such that it can locate `libpayload.so` at runtime without relying on the `LD_LIBRARY_PATH` environment variable. Modify the `Makefile` to correctly embed the library path (e.g., using RPATH) so the daemon successfully starts.

2. **Reconfigure the Services:**
The `nginx` reverse proxy is supposed to forward traffic to the C daemon, but it is currently returning 502 Bad Gateway errors once the daemon is running. Inspect `nginx/nginx.conf` and the daemon's source code. You will find a port mismatch. Adjust the `nginx.conf` file to point to the correct port that the C daemon binds to, and restart the services.

3. **Implement the Payload Filter (Adversarial Corpus):**
The C daemon uses `int validate_payload(const unsigned char *data, size_t len);` from `libpayload.so` to determine if a payload should be accepted (returns 1) or dropped (returns 0). The current implementation accepts everything. 
You must update `src/payload_filter.c` to enforce the following binary protocol rules:
- The first 4 bytes must exactly match the magic number `0xDEADBEEF` (Big Endian).
- The next 4 bytes represent the payload length (Big Endian unsigned integer). This length must exactly match the remaining bytes of the data buffer (i.e., `len - 8`).
- The payload is considered "evil" and must be rejected (return 0) if it violates these rules. Otherwise, it is "clean" (return 1).

We have provided two directories containing test corpora:
- `/home/user/corpora/clean/`: Contains valid binary payloads.
- `/home/user/corpora/evil/`: Contains malformed payloads (wrong magic, truncated, or padded).

Once you have fixed the linking, reconfigured nginx, and implemented the filter, compile your code. Your implementation will be verified by a test script that pushes the corpora through the `nginx` reverse proxy. 

Please create a log file at `/home/user/iot_pipeline/build.log` capturing the output of your successful `make` command to signal you are ready for verification.