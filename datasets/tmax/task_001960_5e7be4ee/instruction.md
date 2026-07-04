You are an engineer investigating a critical memory leak in a mathematical background service.

System Overview:
We have a Python-based service located in `/home/user/poly_service`. This service wraps a highly optimized, compiled mathematical engine (a stripped binary) located at `/app/poly_solver`. The binary computes the complex roots of high-degree polynomials.

The Python service receives requests (lists of polynomial coefficients) via a local unix socket (`/tmp/poly.sock`), invokes the binary, and returns the results. 

Recent deployments have shown that the Python service's memory usage grows unbounded over time, eventually causing the system's OOM killer to terminate it.

Your tasks are:
1. **Environment Repair:** The service currently crashes immediately upon startup. Diagnose and fix the environment or configuration issue so that `python server.py` runs successfully and binds to `/tmp/poly.sock`.
2. **Fuzz Testing:** Write a fuzzing script to blast the service with thousands of random polynomial queries to reliably reproduce the memory leak in a short amount of time.
3. **Bisection:** The repository at `/home/user/poly_service` is a Git repository. We know the leak was introduced sometime in the last 20 commits. The tag `v1.0-stable` is known to be good (no memory leak), while `HEAD` is bad. Use `git bisect` along with your fuzzer to identify the exact commit that introduced the memory leak.
4. **Resolution:** Once you have identified the root cause of the memory leak, patch `server.py` on the `main` branch to completely eliminate it. The service must function correctly without indefinitely consuming memory.

Acceptance Criteria:
- The service must run and correctly serve requests via `/tmp/poly.sock`.
- The memory leak must be completely patched.
- An automated benchmark will start your patched `/home/user/poly_service/server.py`, send it 10,000 random requests, and monitor its Peak RSS (Resident Set Size).
- To pass, the Peak RSS of the Python process during the benchmark must remain under 50 MB.
- Do not change the overall architecture or bypass the binary. Keep the logic intact but fix the leak.

You may use standard terminal tools and write any auxiliary Python/Bash scripts you need.