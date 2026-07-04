You are an open-source maintainer reviewing a pull request (PR) for our project "FastEncodeProxy". The PR introduces a new C-based Python extension for a custom data structure that handles complex character encodings, wrapped in a Flask API, and fronted by an Nginx reverse proxy. 

However, the PR is broken and has several issues:
1. The Nginx reverse proxy configuration is missing crucial routing rules, preventing end-to-end communication to the Flask API.
2. The C extension (`fast_encode.c`) has memory safety issues (undefined behavior and memory leaks) that cause the Flask app to crash or consume excessive memory under load.
3. The Python test fixtures in `tests/test_api.py` are incomplete and do not properly mock the backend data source.

Your task:
1. **Fix the C extension**: Repair the memory leaks and undefined behavior in `/home/user/app/src/fast_encode.c`. The extension implements a custom Trie data structure for fast character encoding conversions.
2. **Reconfigure Nginx**: Update `/home/user/app/nginx.conf` so it correctly routes traffic from port 8080 to the Flask app running on port 5000.
3. **Complete the Test Fixtures**: Update `/home/user/app/tests/test_api.py` to properly mock the external data dependencies using Python's `unittest.mock`.
4. **Compile and Run**: Recompile the C extension, start the Nginx and Flask services, and ensure the system is stable.

A load test script at `/home/user/app/load_test.py` will be used to verify the performance and stability. 
To succeed, the load test must report a throughput of at least 500 requests per second with a memory growth of less than 5MB over 10,000 requests. Ensure the services remain running.