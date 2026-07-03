You are a release manager preparing a new Python-based API service for deployment. Before creating the final release candidate, you need to fix a broken build configuration, implement strict rate limiting, and resolve a memory leak in the core service.

The project is located in `/home/user/release_prep`. 

Here are your objectives:

1. **Build System & Linking**: 
   The application relies on a C extension for token validation located in `src/token_validator.c`. The provided `setup.py` is broken and fails to compile the extension because it is missing a required math library linkage (the C code uses `pow()` and `sqrt()`). Fix `setup.py` so that running `python3 setup.py build_ext --inplace` successfully compiles the `token_validator` module.

2. **Request Validation & Rate Limiting**:
   Modify the main server script `src/app.py`. Implement a basic rate limiter for the `process_request(token)` function. The system must only allow exactly **5 requests per rolling 1-second window** globally. Any requests beyond this limit within a 1-second window must raise a `RateLimitExceeded` exception (which you should define). 

3. **Memory Debugging**:
   The `src/app.py` script contains a memory leak. Every incoming token is appended to a global list called `HISTORY`. In a high-throughput environment, this will crash the container out of memory. Fix this leak by ensuring that the `HISTORY` list acts as a bounded buffer that **only retains the most recent 20 tokens**. Older tokens must be discarded.

4. **Verification**:
   Once you have fixed the build, implemented the rate limiter, and fixed the memory leak, write a test script at `/home/user/release_prep/verify.py` that:
   - Imports `app.py` and `token_validator`.
   - Simulates 10 rapid calls to `process_request("test_token")` in a tight loop.
   - Catches the `RateLimitExceeded` exceptions.
   - Writes the total number of successful requests and the final size of the `HISTORY` list to `/home/user/release_prep/test_results.txt` in the format: `Successful: X, History Size: Y`.

Ensure all code changes are saved and the final text file is created. Do not change the existing functional signatures in `app.py` unless explicitly instructed, just modify their internal logic.