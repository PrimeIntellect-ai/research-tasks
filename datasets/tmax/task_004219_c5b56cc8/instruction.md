You are acting as a systems programmer troubleshooting a performance and linking issue in a distributed job scheduling system. 

The system runs in `/home/user/app/` and consists of three components:
1. A Redis server (running on port 6379) used as a message queue.
2. A Flask web API (`/home/user/app/api.py`, port 5000) that accepts constraint satisfaction jobs (DAG dependencies).
3. A Python worker (`/home/user/app/worker.py`) that pops jobs from Redis and computes the optimal scheduling using a high-performance C library (`/home/user/app/clib/scheduler.c`).

Currently, the system is broken and slow:
1. **Linking Issue:** The C library `libscheduler.so` fails to load in `worker.py` because of an ABI mismatch and missing symbol exports in the C code, along with incorrect `ctypes` definitions in Python.
2. **Data Structure Flaw:** The custom graph data structure passed via FFI between Python and C is defined incorrectly in `worker.py`. It causes memory corruption and severe overhead when marshalling the constraints.
3. **Performance:** Even if it runs, the system is too slow.

Your tasks:
1. Fix the compilation of `/home/user/app/clib/scheduler.c` to properly build `libscheduler.so`. Modify the C code if necessary to ensure symbols are exported correctly.
2. Fix `worker.py` to correctly map the C struct using Python's `ctypes`. The C struct `Graph` contains an array of `Node` constraints. You must design the Python side to pass this efficiently without crashing.
3. Ensure the Flask API, Redis, and worker can communicate correctly.
4. Optimize the FFI boundary to process constraints quickly.
5. Once running, create a test script `/home/user/app/integration_test.py` that submits 5,000 jobs to the Flask API and waits for them to complete. Output the total execution time to `/home/user/app/perf.log` as a single floating-point number representing seconds.

The automated verification will run your `integration_test.py` while the services are up. Your optimization must result in an execution time of less than 1.5 seconds for the 5000 jobs.