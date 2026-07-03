You are an integration developer tasked with securing and deploying a new API gateway environment. 

You have been provided a partially complete workspace in `/home/user/workspace/`. Your goal is to fix the API's build system, configure the system services to route traffic properly, and implement a custom security classifier to block malicious payloads.

### Stage 1: Fix the Build System
In `/home/user/workspace/api/`, there is a Python FastAPI application that relies on a custom C-extension (`fastparser`) for high-performance payload parsing.
The `setup.py` is currently broken and fails to compile because it is missing the correct include directories and compiler flags for the C extension. 
1. Fix the `setup.py` so that the module compiles successfully.
2. Install the package into the local environment (`pip install -e .`).

### Stage 2: Service Composition
The system relies on three services that must run simultaneously:
1. **Redis**: Must run on `127.0.0.1:6379`.
2. **Python API**: Run the FastAPI app (`uvicorn main:app --port 5000`) on `127.0.0.1:5000`. It requires an environment variable `REDIS_URL=redis://127.0.0.1:6379/0`.
3. **Nginx**: A configuration file is located at `/home/user/workspace/nginx/nginx.conf`. You must edit it to listen on port `8080` and proxy all requests to the Python API on port `5000`. Start Nginx using this config.

### Stage 3: The Security Classifier (State Machine & Parser)
The API receives custom key-value payloads. You must write a standalone executable (in any language you choose) located exactly at `/home/user/classifier`.
The executable will be invoked as: `/home/user/classifier <path_to_payload_file>`
It must read the file and determine if it is "Clean" or "Evil".

**Payload Format & Rules:**
- The file contains line-separated key-value pairs (e.g., `username=admin`).
- Values may contain escape sequences: `\n` (newline), `\t` (tab), `\\` (literal backslash), and `\xNN` (2-digit hex representation of an ASCII character).
- **Evil Condition**: A payload is EVIL if, *after* resolving all escape sequences, any value contains the exact substring `EXEC_PAYLOAD` or `DROP_DB`. 
- **Clean Condition**: If the unescaped values do not contain these strings, it is CLEAN.
- Your program must `exit 0` for clean files, and `exit 1` for evil files.

*Hint:* You will need to implement a small state machine or parser to correctly unescape the `\xNN` characters before checking for the blacklisted substrings, as attackers will use escapes to obfuscate their payloads (e.g., `\x45XEC_PAYLOAD`).

### Stage 4: Integration
The Python API uses your classifier. Ensure the API is started with the environment variable `CLASSIFIER_CMD=/home/user/classifier`.

You can test your classifier against the corpora located in `/home/user/workspace/corpus/clean/` and `/home/user/workspace/corpus/evil/`. A successful solution must correctly classify 100% of both corpora. Leave all services running when you finish.