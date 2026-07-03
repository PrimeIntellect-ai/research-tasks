You are a security researcher analyzing a suspicious data processing pipeline. The system uses a proprietary, compiled binary to parse telemetry data, but it has been crashing repeatedly due to malformed payloads.

Your objective is to fix the environment, isolate the crash trigger, and build a resilient Python wrapper service.

Here is the setup:
1. **The Target Binary**: A stripped, packed binary is located at `/app/telemetry_parser`. It expects raw binary data on `stdin` and outputs JSON to `stdout`.
2. **The Data**: 
   - `/home/user/valid_telemetry.dat` contains a working example of the input format.
   - `/home/user/crashing_telemetry.dat` contains a large batch of corrupted input that causes the binary to crash (Segmentation fault).
3. **The Python Environment**: You have a workspace at `/home/user/project/` containing a `requirements.txt` file.

**Task Requirements:**

**Step 1: Environment Setup**
The `requirements.txt` in `/home/user/project/` contains conflicting dependency versions. Resolve the conflicts so that `Flask` and `gunicorn` can be successfully installed. Create a virtual environment at `/home/user/project/venv` and install the resolved dependencies.

**Step 2: Binary Analysis & Delta Debugging**
The `/app/telemetry_parser` binary is packed. Unpack it and use reverse engineering tools (`objdump`, `strings`, `xxd`, etc.) alongside delta debugging on `/home/user/crashing_telemetry.dat` to figure out exactly what byte sequence causes the crash. 
Write your findings to `/home/user/project/crash_analysis.txt`. This file must contain:
- The exact hexadecimal representation of the minimal crashing byte sequence.
- A one-sentence explanation of the vulnerability (e.g., what the binary attempts to do when encountering those bytes).

**Step 3: Resilient Proxy Service**
Write a Python HTTP service at `/home/user/project/proxy.py` that acts as a safe wrapper around the binary. 
The service MUST:
- Listen on exactly `127.0.0.1:8080`.
- Expose a `POST /api/v1/parse` endpoint.
- Accept raw binary data in the HTTP request body.
- **Sanitize** the input: You must write Python code that parses the data stream and filters out the specific corrupted/malicious records identified in Step 2, applying intermediate assertions to ensure the data is safe.
- Pipe the sanitized binary data to `/app/telemetry_parser` via standard input.
- Read the JSON output from the binary and return it as the HTTP response with a `200 OK` status and `application/json` content type.
- If the binary fails or outputs invalid JSON, return a `500 Internal Server Error`.

Start your proxy service in the background and ensure it is listening before you complete the task. Do not assume any authentication is required. Use only standard CLI tools, Bash, and Python to complete this task.