You are a systems programmer managing a local testing pipeline for a hardware emulator. The current CI/CD pipeline is broken due to a C library linking issue, and the telemetry reporting system is missing a required reverse proxy. 

Your objective is to fix the build pipeline, ensure the emulator runs, and implement a lightweight Python reverse proxy to route the CI telemetry correctly.

Here is the current state of the workspace in `/home/user/`:
1. `/home/user/device.c` - A C source file simulating a hardware component. It uses functions from the math library.
2. `/home/user/build.sh` - A shell script acting as our CI compilation step. It attempts to compile `device.c` into a shared library `libdevice.so`, but it currently fails or produces a library with undefined symbols because it doesn't link the standard math library.
3. `/home/user/emulator.py` - A Python script simulating the device. It uses `ctypes` to load `./libdevice.so` and execute `compute_sensor(0.0)`. It then sends an HTTP POST request with the result to `http://localhost:8080/submit`.
4. `/home/user/ci_server.py` - A mock backend CI server that listens on `http://localhost:9090`. It expects POST requests and writes the output and headers to `/home/user/ci_results.json`.

Your tasks:
1. **Fix the Linking Issue**: Modify `/home/user/build.sh` so that it successfully compiles `device.c` into `libdevice.so`. Ensure that all necessary system libraries are dynamically linked (specifically the math library) so the Python emulator can load it without "undefined symbol" errors.
2. **Implement a Reverse Proxy**: The emulator sends data to port 8080, but the CI server listens on port 9090. Create a Python script at `/home/user/proxy.py` that acts as a simple reverse proxy.
   - It must listen on `localhost` port `8080`.
   - It must accept `POST` requests.
   - It must forward the request body exactly as received to `http://localhost:9090` (the path does not matter for the backend server, just forward to the root or the same path).
   - Crucially, it must add a new HTTP header to the forwarded request: `X-Proxy-Routed: 1`.
   - It should return a 200 OK status back to the emulator.
3. **Execute the Pipeline**: 
   - Run `/home/user/build.sh` to generate `libdevice.so`.
   - Start the backend server `/home/user/ci_server.py` in the background.
   - Start your proxy `/home/user/proxy.py` in the background.
   - Run `/home/user/emulator.py`.

If successful, the backend server will automatically write `/home/user/ci_results.json`. Leave this file in place as it will be used for automated verification.