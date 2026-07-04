You are an integration developer tasked with testing a new API rate-limiting shared library. The library was written in C++ but is meant to be loaded by a Python API gateway simulator.

Currently, the C++ project has an ABI/linking mismatch preventing Python's `ctypes` from easily interacting with its exposed function, and the build setup is rudimentary. 

Your objectives:
1. Fix the code and/or Makefile in `/home/user/src/` so that it successfully compiles into a shared library (`libratelimit.so`) with a standard C ABI (no C++ name mangling for the target function). You can use standard Linux tools (like `nm` or `objdump`) to analyze the generated object files and ensure the exported symbol is correct.
2. Write a Python script at `/home/user/test_api.py` that loads `/home/user/src/libratelimit.so` via `ctypes`.
3. The C++ library provides a function with the signature `int allow_request(uint32_t client_id, uint32_t max_reqs)`. It increments an internal counter for the `client_id` and returns `1` if the counter is less than or equal to `max_reqs`, and `0` otherwise.
4. Your Python script must read incoming requests from `/home/user/requests.txt`.
5. For each line in the file:
   - **Request Validation**: Check if the line strictly follows the format `CLIENT_ID:PAYLOAD` (where `CLIENT_ID` is a positive integer). If a line is malformed, completely ignore and drop it (do not log it).
   - **Rate Limiting**: Extract the `CLIENT_ID` and call `allow_request(client_id, 2)` (setting a hardcoded limit of 2 requests per client).
   - **Logging**: If the shared library allows the request, write `ACCEPTED: <original_line>` to `/home/user/api_results.log`. If it rejects the request due to rate limiting, write `REJECTED: <original_line>` to the same log file. Note: The `<original_line>` should be exactly as it appeared in the input, but strip trailing newlines in the log.

You must run your build step, verify the shared library works, and execute your Python script so that `/home/user/api_results.log` is fully populated.