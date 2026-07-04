You are acting as a support engineer. We have a Python-based background service called `math_service.py` located in `/home/user/math_service.py` that processes numerical telemetry data via a REST API. 

Recently, we've noticed intermittent HTTP 500 errors and crashes in production. We have captured the problematic traffic patterns in a simulator script located at `/home/user/traffic_gen.py`.

Your task is to diagnose and fix the bugs in `math_service.py`. The service suffers from three distinct categories of issues:
1. **Format Parsing Edge-Cases:** The service occasionally fails to parse incoming numbers because some legacy clients send string representations of floats with thousands separators (e.g., `"1,234.56"`).
2. **Numerical Instability:** The calculation used for standard deviation is highly susceptible to catastrophic cancellation when processing numbers with very small variance but large magnitudes (e.g., `100000000.01` and `100000000.02`), causing `math.sqrt()` to throw a `ValueError`.
3. **Concurrency:** The service updates global state across multiple threads without synchronization, leading to race conditions and incorrect running totals under concurrent load.

**Instructions:**
1. Analyze `/home/user/math_service.py` and run `/home/user/traffic_gen.py` alongside it to inspect the errors.
2. Fix the issues in the service script. You must:
   - Gracefully handle strings with commas before converting to float.
   - Replace the naive variance calculation with a numerically stable approach (e.g., Welford's algorithm or an equivalent stable formulation).
   - Ensure thread-safe updates to the global state.
3. Save your corrected code to `/home/user/fixed_math_service.py`. 

The automated test will verify your solution by running `/home/user/fixed_math_service.py` and sending a rigorous barrage of edge-case and concurrent requests to ensure it returns valid HTTP 200 responses with the correct standard deviation without crashing.