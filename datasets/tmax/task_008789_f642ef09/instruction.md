You are a systems programmer and security engineer tasked with debugging and fixing a critical microservice. 

You have been given access to a Python project located at `/home/user/sec_ws`. This project runs a WebSocket server that receives binary authentication tokens. To maximize performance, the deserialization of these tokens is implemented in a C extension. Furthermore, the application relies on gRPC protobuf definitions for the token structure.

Currently, the project is completely broken:
1. **Build System & Linking:** The `setup.py` file is misconfigured. When you try to build the C extension (`python3 setup.py build_ext --inplace`), it fails. You need to identify the linking/configuration issue in `setup.py` and fix it so the module `fast_auth` compiles successfully.
2. **gRPC/Protobuf:** The protobuf file `proto/auth.proto` has not been compiled into Python code. You must compile it so that the resulting `auth_pb2.py` file is located directly in `/home/user/sec_ws`.
3. **C Memory Safety (Security Vulnerability):** The C extension (`src/deserializer.c`) contains a severe memory safety vulnerability (Out-of-Bounds read/Buffer Overflow) when parsing malicious or malformed payload lengths. A specially crafted WebSocket message can crash the server via a Segmentation Fault. You must fix the C code. If the claimed length of the token in the binary payload exceeds the actual remaining bytes, the function should set a Python `ValueError` with the message `"Invalid token length"` and return `NULL` to safely propagate the exception to Python.
4. **WebSocket & Serialization test:** We have provided a test script `test_server.py` in the directory. It stands up the WebSocket server, connects to it, and sends both valid protobuf messages and malicious binary payloads designed to trigger the C bug.

**Your objectives:**
1. Fix `setup.py`.
2. Compile `proto/auth.proto`.
3. Fix the memory vulnerability in `src/deserializer.c`.
4. Compile the extension.
5. Run `python3 test_server.py`. If successful, the script will output a success hash. Write this exact success hash to a file at `/home/user/result.log`.

Do not modify `test_server.py` or `proto/auth.proto`.