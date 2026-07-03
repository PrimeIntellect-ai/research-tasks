You are an engineer tasked with porting a legacy C-based constraint satisfaction solver to a minimal containerized Python microservice. 

We have a vendored C extension for Python located at `/app/cspsolver-0.1.0`. This package provides a fast backend for solving mathematical matrix constraints, but it currently has two major problems:
1. It crashes randomly in minimal environments due to a memory safety bug (Undefined Behavior) in `solver.c`.
2. It is too slow to meet our microservice latency requirements.

Your tasks:
1. **Fix the C Extension**: Inspect `/app/cspsolver-0.1.0/solver.c`. Find and fix the memory safety bug (an out-of-bounds array access that causes segmentation faults on large matrices).
2. **Optimize**: The `setup.py` is misconfigured for performance. Modify it to compile with standard C compiler optimization flags so it runs significantly faster.
3. **Install**: Install the fixed package into the current Python environment.
4. **Build the REST API**: Write a Python script at `/app/server.py` using `FastAPI` (and `uvicorn`) that exposes the solver.
    * Endpoint: `POST /solve`
    * Request Body (JSON): `{"matrix": [[int, ...], ...]}` (A 2D array of integers)
    * Response Body (JSON): `{"solution": [[int, ...], ...]}` or `{"error": "string"}` if invalid.
    * The API must call the `cspsolver.solve(matrix)` function from the extension.
5. **Benchmark**: The server must run on port 8000. Run the provided benchmark tool `/app/benchmark.py` against your running server. The API must handle all requests without crashing, and the average latency must be strictly less than **15.0 milliseconds** per request. 

Ensure your final server code is saved at `/app/server.py` and runs successfully. You do not need to keep the server running after you have tested it; our automated verifier will start it and run its own benchmark.