I'm working on a performance-critical request validation service. We currently have a pure Python rate limiter, but it's too slow for our throughput requirements. I started porting the token bucket rate limiting logic to C to be used via `ctypes` (FFI), but the project is currently broken.

Here is the current state of the project in `/app/`:
1. `/app/rate_limit_specs.png` - An image from our design team detailing the exact capacity and refill rate required for the rate limiter. You will need to extract these parameters to correctly configure the C implementation.
2. `/app/ratelimit.c` - The skeleton C implementation. It is missing the actual token bucket logic and the necessary FFI export directives. Also, it has a conditional compilation block that requires the macro `OPTIMIZED_BUILD` to be defined during compilation to enable the fast path.
3. `/app/Makefile` - The build script. It's broken: it fails to produce a proper shared library (`libratelimit.so`), lacks Position Independent Code (`-fPIC`) flags, and doesn't define the required macro.
4. `/app/validator.py` - The Python script that validates incoming requests. It contains the slow `PurePythonRateLimiter` and an incomplete `CRateLimiter` class. You need to finish the `CRateLimiter` class to load the shared library and map the C functions properly.
5. `/app/benchmark.py` - A benchmarking suite that compares the Python and C implementations, checks correctness against the specs, and outputs a performance ratio.

Your task:
1. Extract the rate limit parameters (Capacity and Refill Rate) from `/app/rate_limit_specs.png`.
2. Fix `ratelimit.c` to implement a standard token bucket algorithm using those parameters. The state can be kept in a simple global struct for this single-threaded benchmark. The signature should be `bool allow_request()`.
3. Fix the `Makefile` so that running `make` cross-compiles/builds a valid `/app/libratelimit.so` shared library with the `OPTIMIZED_BUILD` macro defined.
4. Update `validator.py` to correctly interface with the C library via `ctypes`.
5. Run `python3 /app/benchmark.py`. If the implementation is correct and optimized, it will write a float representing the speedup multiplier to `/app/speedup.txt`.

Our CI pipeline will verify your implementation by reading `/app/speedup.txt`. The C implementation must be functionally correct and achieve a speedup of at least 5.0x over the pure Python version.