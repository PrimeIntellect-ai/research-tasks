You are helping migrate a legacy data processing pipeline from Python 2 to Python 3, while also hardening its API gateway. The system consists of a Go-based reverse proxy, a Python API backend, and a C-extension used by Python for a custom fast-lookup data structure (a Prefix Trie).

Currently, the system is broken and failing to start or properly filter requests. Your objective is to fix the build, update the code, implement validation, and configure the services to pass an adversarial test suite.

Here is the system layout under `/home/user/app/`:
- `proxy/`: Contains a Go API gateway (`main.go`). It should run on port 8080 and forward to Python on 8081.
- `backend/`: Contains the Python backend (`server.py`). It was written in Python 2 and needs porting to Python 3.
- `backend/ctrie/`: Contains the C-extension. It uses `CMakeLists.txt` but currently fails to build because it can't find the Python shared library at link time, and has a syntax error due to Python 3 API changes.
- `corpora/`: Contains two directories, `clean/` and `evil/`, full of JSON payloads.
- `start.sh`: A script that compiles the C extension, builds the Go proxy, and starts both services.

Your tasks:
1. **Fix the C Extension Build:** The `CMakeLists.txt` in `/home/user/app/backend/ctrie/` is misconfigured. It fails to link the Python 3 libraries. Fix the CMake configuration so `make` successfully builds `ctrie.so`. 
2. **Migrate to Python 3:** Update `/home/user/app/backend/server.py` and the C-extension bindings to be Python 3.x compatible.
3. **Go Proxy Rate Limiting & Concurrency:** Edit `/home/user/app/proxy/main.go`. Implement a rate limiter using Go channels and goroutines that restricts requests to a maximum of 5 per second globally. Excess requests must immediately return HTTP 429 Too Many Requests.
4. **Request Validation:** Update the Go proxy to inspect the JSON body. Reject any payload where the `"query"` field contains the exact substring `'OR 1=1'` or where `"is_admin"` is set to `true`. Rejected payloads must return HTTP 403 Forbidden. Valid payloads must be forwarded to the Python backend.

You must ensure that running `/home/user/app/start.sh` successfully brings up the Go proxy on `127.0.0.1:8080` and Python backend on `127.0.0.1:8081`.

Verification:
We will run an automated tester against `127.0.0.1:8080`. 
- It will send all JSON files from `/home/user/app/corpora/clean/` at a rate of 2 req/sec. Your system MUST return HTTP 200 OK for 100% of these.
- It will send all JSON files from `/home/user/app/corpora/evil/` at a rate of 2 req/sec. Your system MUST return HTTP 403 Forbidden for 100% of these.
- It will blast 20 concurrent requests. Exactly 5 must succeed (or return 403 depending on payload), and the rest MUST return HTTP 429.

Ensure the final working state is running and listening on port 8080. Leave the services running in the background.