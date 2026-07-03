You are a support engineer responding to an urgent escalation. Our distributed mathematical computation pipeline (which computes high-precision matrix operations) is producing wildly inaccurate results and intermittently crashing under load. 

The pipeline consists of three services:
1. **Redis Cache** (port 6379)
2. **C Math Backend** (port 8001) - A custom C daemon that performs the heavy lifting.
3. **Python API Gateway** (port 8000) - A Flask service that receives user requests, passes them to the C backend over TCP, and caches successful results in Redis.

All services can be started via the provided script: `/app/start_all.sh` (this spins them up in the background).

Your diagnostic and repair tasks are as follows:

**1. Secret Recovery**
The C backend was recently refactored to read a critical mathematical calibration constant from an environment variable. However, the developer forgot to provide the new configuration, and the old hardcoded constant was removed from the code.
- Investigate the Git repository located at `/app/services/backend_c`.
- Find the removed calibration constant (a 32-bit hex value).
- Create a file at `/home/user/config.env` containing exactly `CALIBRATION_KEY=<your_recovered_hex_value>`. Our startup script automatically sources this file.

**2. Dependency Conflict Resolution**
The C backend is currently producing incorrect floating-point results. Diagnostics suggest it is dynamically linking against an old, buggy version of our proprietary math library (`libmatrix_v1.so`) instead of the correct version (`libmatrix_v2.so`). Both are located in `/app/libs/`.
- Inspect `/app/services/backend_c/Makefile` and any relevant source files.
- Resolve the dependency conflict so that the backend compiles and links against `libmatrix_v2.so` without breaking the build.
- Recompile the C backend.

**3. Crash Diagnostics via Fuzzing**
We suspect the C backend has a segmentation fault when parsing malformed binary headers.
- Write a bash script to fuzz the C backend TCP socket (port 8001) using standard CLI tools (e.g., `nc`, `/dev/urandom`, `dd`).
- Once you successfully trigger a crash (the backend process will die and drop the connection), identify the exact sequence of bytes that caused the crash.
- Save the hex-encoded representation of a minimal crashing payload to `/home/user/crash_input.hex`.

**4. Verification**
Once you have restored the key, fixed the dependency, recompiled, and restarted the services (using `/app/start_all.sh`), you must verify the mathematical accuracy of the pipeline.
- Run the evaluation suite: `python3 /app/evaluate_mse.py`
- This script sends 100 random matrices to the API gateway (port 8000) and calculates the Mean Squared Error (MSE) compared to a known-good reference.
- You must achieve an `MSE < 0.001` to consider the system fully repaired. 

Please proceed with diagnosing and fixing the pipeline.