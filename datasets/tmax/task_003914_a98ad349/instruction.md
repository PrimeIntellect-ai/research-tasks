I am an open-source maintainer reviewing a PR for our Python data processing service. The contributor added a C-extension for performance, but the PR is failing in our CI environment. Locally it supposedly passes, but in CI it's broken.

The project is located at `/home/user/project/`. 

Here is what's failing:
1. The CI environment doesn't have the compiled protobuf files. You need to install the necessary Python packages and generate the gRPC Python code from `service.proto`.
2. The `Makefile` provided by the contributor is completely broken for building a shared library. It currently fails to create a valid `.so` file that Python's `ctypes` can load. You need to repair the `Makefile` to properly compile `fast_parser.c` into a shared library named `libfastparser.so` (ensure it uses position-independent code and links as a shared object).
3. Once the gRPC files are generated and the shared library is correctly built via `make`, the test script `test_server.py` should be able to run.

Your task:
1. Fix the `Makefile` so that running `make` successfully builds `libfastparser.so`.
2. Generate the gRPC Python files (`service_pb2.py` and `service_pb2_grpc.py`) from `service.proto`.
3. Run the test script using `python3 /home/user/project/test_server.py` and redirect its standard output to `/home/user/result.log`.

Ensure all dependencies are met and the final output log is correctly populated.