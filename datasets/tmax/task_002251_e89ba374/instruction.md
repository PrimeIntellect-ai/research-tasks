I am migrating an old Web Application Firewall (WAF) microservice from Python 2 to Python 3. The service receives payloads via gRPC and passes them to a high-speed C-shared library (`libmatcher.so`) to check for malicious signatures. 

Currently, the setup is broken for Python 3. The gRPC protobuf files haven't been generated for Python 3, and the Python server code crashes or throws type errors when interacting with the C library under Python 3 due to ABI/type changes between the language versions.

The working directory is `/home/user/waf`.

Please complete the following migration tasks:
1. Create a Python 3 virtual environment at `/home/user/waf/venv` and install the required gRPC packages for Python 3 (`grpcio`, `grpcio-tools`).
2. Generate the Python 3 gRPC and protobuf bindings from `/home/user/waf/waf.proto` into the `/home/user/waf` directory.
3. Modify `/home/user/waf/server.py` so that it is fully compatible with Python 3. Pay special attention to how Python 3 handles strings versus bytes when passing data to the C library via `ctypes`.
4. Start the gRPC server in the background.
5. Run the provided `/home/user/waf/test_client.py` using your virtual environment's Python, and redirect its standard output to `/home/user/waf/migration_result.txt`.

Ensure the final `migration_result.txt` file exists and contains the successful boolean evaluations of the test payloads.