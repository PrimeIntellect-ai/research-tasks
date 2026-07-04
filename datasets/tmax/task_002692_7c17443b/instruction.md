You are tasked with fixing and optimizing a high-performance custom bytecode evaluation API. 

The system consists of three services:
1. An Nginx reverse proxy listening on port 8080.
2. A Python Flask backend running via Gunicorn on port 5000.
3. A Redis server on port 6379 for result caching.

The Python backend evaluates a custom stack-based bytecode. Currently, it delegates the execution to a highly concurrent Go library (`vm.go`) compiled as a C-shared library (`libvm.so`). However, the system is currently broken due to FFI/linking issues, and it's severely underperforming.

Your objectives are:
1. **Fix the Go Build & Concurrency**: The Go code in `/app/go_vm/vm.go` has a concurrency bug when handling batch requests, and its Makefile is misconfigured. Fix the code to safely use goroutines/channels without race conditions, and correctly compile it to `/app/lib/libvm.so`.
2. **Fix Python C-Bindings**: The Python wrapper in `/app/backend/ffi.py` has incorrect `ctypes` declarations, causing segmentation faults and incorrect return values. Fix the `argtypes` and `restype` definitions. Note that the Go C-string returned must be freed to avoid memory leaks.
3. **Configure Nginx & Redis**: Ensure Nginx (`/etc/nginx/sites-available/default`) correctly proxies `/api/` requests to `http://127.0.0.1:5000/`. Ensure the Flask app (`/app/backend/app.py`) uses Redis (at `127.0.0.1:6379`) to cache identical bytecode execution results for 60 seconds.
4. **Benchmarking**: The final system must achieve high throughput. An evaluation script `/app/benchmark.py` will be used by the verifier to measure the requests per second (RPS) of your system through the Nginx proxy.

**Acceptance Criteria**:
- All services (Nginx, Gunicorn, Redis) must be running and communicating properly.
- The API endpoint `POST /api/execute` accepts JSON: `{"batch": ["PUSH 5 PUSH 10 ADD", "PUSH 3 PUSH 4 MUL"]}` and returns `{"results": ["15", "12"]}`.
- The system must pass the automated benchmark with a measured throughput of **>= 800 Requests Per Second (RPS)**.

All code is located in `/app/`. You must restart the system services (`sudo systemctl restart nginx`, etc., or the provided script `/app/restart_services.sh`) after applying your fixes. Ensure your C-shared library is placed exactly at `/app/lib/libvm.so`.