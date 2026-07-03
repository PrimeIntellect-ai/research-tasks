You are acting as a Release Manager preparing the new `compute_node` backend for deployment.

We have a proprietary Python extension called `fastalgo` that wraps a core C++ shared library. The source code for this extension is vendored at `/app/fastalgo`. However, the build pipeline is currently broken. The CMake configuration inside the package fails to locate and link the shared library located at `/app/proprietary/libalgo.so` during the wheel build process. 

Your task consists of three phases:

**Phase 1: Fix and Install the Vendored Package**
1. Inspect the CMake build configuration of the vendored package at `/app/fastalgo/CMakeLists.txt`.
2. Fix the CMake configuration so that it correctly links against the pre-compiled shared library located at `/app/proprietary/libalgo.so`. You will likely need to adjust link directories, library names, or target link properties.
3. Once fixed, build and install the `fastalgo` package into the active Python environment. (Note: Ensure the system can find `libalgo.so` at runtime, for example by utilizing `LD_LIBRARY_PATH` or compiling with an appropriate rpath).

**Phase 2: Implement the Compute Node Service**
Create a Python service script at `/app/compute_node.py` that utilizes the newly installed `fastalgo` package. The service must handle two different protocols to integrate with our orchestration mesh:

1. **HTTP REST API (Port 8080)**
   - Listen on `0.0.0.0:8080`.
   - Expose a `POST /process` endpoint.
   - The endpoint should expect a JSON payload in the format `{"input": <integer>}`.
   - It must call `fastalgo.process_data(<integer>)` and return an HTTP 200 response with the JSON payload: `{"status": "success", "output": <result_from_fastalgo>}`.

2. **TCP Health/Telemetry Socket (Port 8081)**
   - Concurrently listen for raw TCP connections on `0.0.0.0:8081`.
   - When a client connects and sends the exact string `HEARTBEAT\n` (encoded in UTF-8), the server must immediately reply with `ALIVE\n` and keep the connection open for further heartbeats.
   - You may use standard libraries like `socket`, `asyncio`, `ThreadingTCPServer`, or a web framework that supports both (like FastAPI with a background socket task).

**Phase 3: Launch**
Run the service in the background and write its process ID (PID) to `/app/service.pid`. Make sure both ports are bound and listening. Leave the service running.

*Constraints & Hints:*
- Use standard Python 3.
- You may install any Python web framework you prefer (e.g., Flask, FastAPI, aiohttp) using pip.
- Do not modify the source code of the `fastalgo` C++ files or the `/app/proprietary/` library. Only modify the build configuration (`CMakeLists.txt` / `setup.py` etc.) and write the `compute_node.py` script.