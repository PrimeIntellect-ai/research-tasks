I am building an integration test suite for our telemetry system, and I need your help writing a C client that interacts with a mock API, serializes test data, and benchmarks the responses.

We have a custom JSON payload that needs to be sent to our API. However, the external dependencies (the actual API server) are offline. I have prepared a local mock server script, but I need you to set up the dependencies, complete the C client implementation, and run a benchmark.

Here is what you need to do:

1. **Dependency Management**: I have placed a source tarball of the `cJSON` library at `/home/user/cJSON.tar.gz`. Extract it, compile it, and make it available so we can link it with our C program. You can build it as a static object (`cJSON.o`) or shared library in `/home/user/cjson_build`.

2. **Mock Server Setup**: I have written a pure Python mock server at `/home/user/mock_server.py`. It listens on `127.0.0.1:9090`. Start this server in the background. It implements a single `POST /telemetry` endpoint.

3. **C Client Implementation**: Write a C program at `/home/user/telemetry_client.c`. 
   - It must use `libcurl` for HTTP communication and the `cJSON` library you built for serialization/deserialization.
   - It needs to send a POST request to `http://127.0.0.1:9090/telemetry` with the `Content-Type: application/json` header.
   - The JSON payload must be exactly: `{"device_id": 808, "measurements": [10, 20, 30, 40, 50, 60]}`
   - The mock server will return a JSON response containing a `processing_time_ms` field.
   - Parse this response and print *only* the integer value of `processing_time_ms` to standard output (e.g., `42\n`).

4. **Benchmarking**: Write a bash script at `/home/user/benchmark.sh`.
   - The script should execute the compiled C program (`/home/user/client`) exactly 50 times in a loop.
   - It should sum up all the `processing_time_ms` values printed by the C program.
   - Finally, it should write the total sum to a file at `/home/user/benchmark_result.txt` in the exact format: `Total Time: <SUM_VALUE>` (e.g., `Total Time: 2100`).

Please ensure the C program handles the memory allocation and cleanup for `cJSON` and `libcurl` properly. Compile the program as `/home/user/client`. Once completed, run your benchmark script to generate the final `benchmark_result.txt` file.