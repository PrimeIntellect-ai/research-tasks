You have recently inherited an unfamiliar codebase for a multithreaded synchronization server. The source code is located at `/app/vendored/py-sync-server-1.0.0`. The server exposes two interfaces: an HTTP API and a raw TCP socket interface. 

Unfortunately, the server is currently non-functional and suffers from several critical bugs:
1. **Deadlock under contention:** The multithreaded request handlers in `server.py` frequently deadlock when processing concurrent requests due to improper lock ordering.
2. **Missing Source / Binary Reverse Engineering:** The core computational logic is located in `compute_utils.pyc`. The original Python source file is missing. You must decompile this bytecode to understand the algorithm.
3. **Convergence Failure / Off-by-one:** Inside `compute_utils`, the `calculate_convergence(data, threshold)` function has an off-by-one boundary error in its loop condition. This prevents the algorithm from converging properly, sometimes causing an infinite loop or returning an incorrect aggregate. Fix this function, ensuring it uses assertion-based intermediate validation to verify that the intermediate delta is strictly decreasing before returning the final state.
4. **Broken Setup:** The `Makefile` provided to run the server contains a configuration error that prevents it from launching with the correct Python interpreter.

Your task:
1. Decompile `compute_utils.pyc`, recover the source as `compute_utils.py`, and fix the convergence boundary error.
2. Fix the locking logic in `server.py` to prevent deadlocks (ensure a consistent lock acquisition order).
3. Fix the `Makefile` so `make run` works successfully.
4. Start the server in the background using `make run`. 

The server must listen on:
- HTTP: `127.0.0.1:8080` (Requires header `Authorization: Bearer secret-token-123`)
- TCP: `127.0.0.1:8081`

Automated tests will verify your fixes by sending highly concurrent requests across both protocols to ensure the deadlock is resolved and the convergence algorithm returns the correct values. Leave the server running when you are finished.