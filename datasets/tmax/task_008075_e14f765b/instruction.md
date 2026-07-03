You have been given a messy directory of project files at `/home/user/workspace`. Your task is to organize this project, compile the necessary components, and implement a gRPC microservice in Python that utilizes a C shared library for mathematical evaluations and data decoding.

Here are the requirements:

1. **Project Organization**:
   Create a clean project structure at `/home/user/project` with the following subdirectories:
   - `/home/user/project/lib` (for compiled shared libraries)
   - `/home/user/project/grpc_gen` (for generated protobuf Python files)
   - `/home/user/project/src` (for Python source code)

2. **Shared Library Management**:
   In `/home/user/workspace`, there is a C file named `calculator.c`. 
   Compile this file into a shared library named `libcalc.so` and place it in `/home/user/project/lib/libcalc.so`.
   The C library exposes a function:
   `int evaluate_hex_expression(const char* hex_str, double* result);`
   This function takes a hex-encoded string (e.g., `"322b32"` for `"2+2"`), decodes it to ASCII, evaluates the simple `A op B` mathematical expression (supports `+`, `-`, `*`, `/` with doubles), and stores the answer in `result`. It returns `0` on success.

3. **gRPC and Protobuf Service**:
   In `/home/user/workspace`, there is a `service.proto` file defining a `MathService` with a `Compute` RPC.
   Compile this protobuf file for Python using `grpc_tools.protoc`. Place the generated `_pb2.py` and `_pb2_grpc.py` files in `/home/user/project/grpc_gen`. Note: Ensure that your Python scripts can import from this directory (e.g., creating an `__init__.py` or manipulating `sys.path`).

4. **Microservice Implementation**:
   Write a gRPC server in Python at `/home/user/project/src/server.py`.
   - The server must listen on `localhost:50051`.
   - It must implement the `MathService.Compute` endpoint.
   - It must load `libcalc.so` using `ctypes` and correctly define the ABI (`argtypes` and `restype`) to call `evaluate_hex_expression`.
   - The RPC takes a `ComputeRequest` with a `hex_payload` field, passes it to the C shared library, retrieves the `double` result, and returns it in a `ComputeResponse`.

5. **Client & Verification**:
   Write a client at `/home/user/project/src/client.py` that connects to the server and sends a `ComputeRequest` with the following `hex_payload`: `"31352e352a332e30"` (which is hex for `"15.5*3.0"`).
   The client should print ONLY the numeric result (formatted to 1 decimal place) to standard output.

6. **Execution**:
   Write a shell script at `/home/user/project/run.sh` that:
   - Starts the server in the background.
   - Waits 2 seconds for it to initialize.
   - Runs the client and redirects the output to `/home/user/project/output.txt`.
   - Kills the background server.
   
Execute your `run.sh` script so that `/home/user/project/output.txt` is populated.

Dependencies:
You may need to install `grpcio` and `grpcio-tools` via `pip`.