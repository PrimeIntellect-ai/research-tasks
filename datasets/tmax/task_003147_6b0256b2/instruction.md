As a mobile build engineer, you are migrating our pipeline telemetrics out of a monolithic codebase to fix circular dependency issues that have been breaking our builds. 

Your task is to create a standalone microservice that calculates build-time statistics. To ensure high performance, the core math must be implemented in a shared library, while the web service can be written in any language of your choice.

Please complete the following in the `/home/user/metrics/` directory (you will need to create it):

1. **Numerical Algorithm & Shared Library:**
   - Write a C or C++ program that implements a function to calculate the *population standard deviation* of an array of double-precision floating-point numbers.
   - Compile this code into a shared object library named `/home/user/metrics/libmetric.so`.
   - The population standard deviation formula is: `sqrt( sum( (x_i - mean)^2 ) / N )`.

2. **Web Service (URL Routing & Parameter Parsing):**
   - Write a web server in any language you prefer.
   - It must listen on `http://127.0.0.1:8181`.
   - It must expose a `GET` endpoint at the path `/stdev`.
   - The endpoint must accept a query parameter `build_times` containing a comma-separated list of numbers (e.g., `/stdev?build_times=10,12.5,23,16`).
   - The server must parse these numbers, pass them to your compiled `libmetric.so` using Foreign Function Interface (FFI) or equivalent shared library loading mechanisms, and retrieve the calculated standard deviation.
   - The endpoint must return a JSON response with the standard deviation rounded to exactly two decimal places. Example response: `{"stdev": 5.24}`.

3. **Integration Testing:**
   - Write an integration test script at `/home/user/metrics/test_integration.sh`.
   - This script should assume the server is already running. It must use `curl` to send a request to `http://127.0.0.1:8181/stdev?build_times=2,4,4,4,5,5,7,9`, parse the JSON response, verify that the `stdev` value is exactly `2.00`, and exit with code `0` on success or `1` on failure.
   - Ensure the script is executable.

You must leave the server running in the background on port `8181` when you are finished so it can be verified.