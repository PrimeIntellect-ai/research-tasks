You are a utility script developer working on a secure API gateway. You have been provided with a partially completed C++ project in `/home/user/api_gateway`. This project builds a command-line utility `gateway_tool` that simulates validating incoming web requests by checking their payload checksums and enforcing rate limits per IP address.

Currently, the project is broken. Your task is to fix the build system, implement the missing C++ logic, and write a Python test script to verify the behavior.

Here are your specific requirements:

1. **Fix the Build System:**
   There is a `Makefile` in `/home/user/api_gateway`. When you run `make`, it compiles the object files but fails during the linking stage. Identify the missing object file in the linking step and fix the `Makefile` so that `make` successfully produces the `gateway_tool` executable.

2. **Implement Checksum Validation:**
   In `/home/user/api_gateway/checksum.cpp`, implement the `uint16_t calculate_fletcher16(const std::string& data)` function. 
   - It must implement the 16-bit Fletcher's checksum.
   - Iterate through each byte (cast to `uint8_t`) of the string.
   - Maintain two 16-bit sums (`sum1` and `sum2`), initialized to 0.
   - For each byte, add it to `sum1`, then modulo 255. Add `sum1` to `sum2`, then modulo 255.
   - Return the combined 16-bit value: `(sum2 << 8) | sum1`.

3. **Implement Rate Limiting:**
   In `/home/user/api_gateway/rate_limit.cpp`, implement the `RateLimiter` class methods.
   - The constructor receives `int max_requests`.
   - The `bool allow_request(const std::string& ip)` method should track how many times it has been called for a specific IP string.
   - If the IP has been seen less than `max_requests` times, increment its count and return `true`.
   - If the IP has reached or exceeded `max_requests`, return `false`.

4. **Write a Test Fixture / Runner:**
   Create a Python script at `/home/user/api_gateway/run_tests.py`.
   This script must execute the compiled `./gateway_tool <ip> <data> <provided_checksum_int>` using the `subprocess` module.
   `gateway_tool` will output exactly one of these strings to standard output:
   - `RATE_LIMITED`
   - `CHECKSUM_FAILED`
   - `ALLOWED`
   
   Your Python script should run the following simulated sequence of requests in order, and append the stdout of each run (stripped of extra newlines) to a log file at `/home/user/gateway_test_results.log`, with one result per line:
   
   - Request 1: IP = "10.0.0.1", Data = "payload_A", Checksum = 16223
   - Request 2: IP = "10.0.0.1", Data = "payload_B", Checksum = 99999 (intentionally bad checksum)
   - Request 3: IP = "10.0.0.1", Data = "payload_C", Checksum = 17513
   - Request 4: IP = "10.0.0.1", Data = "payload_D", Checksum = 17772
   - Request 5: IP = "10.0.0.1", Data = "payload_E", Checksum = 18031

Ensure you compile the fixed code, run the Python test script, and verify that `/home/user/gateway_test_results.log` is generated with exactly 5 lines corresponding to the expected outputs of the 5 requests.