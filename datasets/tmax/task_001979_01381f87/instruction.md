You are tasked with organizing and rescuing a fragmented multi-language data processing project. The previous developer left behind an architectural mess with conflicting dependencies, and we need you to build a clean, unified pipeline that processes data through a reverse proxy, a Go gRPC service, and a highly optimized C library.

Your objective is to build this pipeline in `/home/user/project`. Create the directory and organize the following components:

**1. C Data Processing Library (`/home/user/project/c_src/`)**
Write a C library (`transform.c` and `transform.h`) containing a function:
`void transform_data(unsigned char* data, int length);`
This function must perform an in-place bitwise XOR operation on every byte of the input array using the key `0x42`. 
Compile this into a shared library named `libtransform.so`.

**2. Protobuf Definition (`/home/user/project/proto/`)**
Create a file `transform.proto` defining a gRPC service named `Transformer`.
It should have an RPC method `Apply` that takes a message `TransformRequest` (containing a single field `bytes payload = 1`) and returns a `TransformResponse` (containing `bytes result = 1`).
Compile this protobuf definition for both Go and Python.

**3. Go gRPC Server (`/home/user/project/go_server/`)**
Write a Go gRPC server (`server.go`) that listens on `127.0.0.1:50051`. 
It must implement the `Transformer` service. Inside the `Apply` method, it must use **CGO** (FFI) to pass the incoming byte payload to the C `transform_data` function, and return the mutated bytes. 
Ensure your Go server leverages standard Go concurrency (gRPC handlers run in their own goroutines natively, but ensure your CGO call is safe). 
Initialize a Go module, fetch dependencies, and build the server binary `server`.

**4. Python Reverse Proxy (`/home/user/project/proxy/`)**
Write a Python HTTP server (`proxy.py`) using the built-in `http.server` module that listens on `127.0.0.1:8080`.
This server must act as a reverse proxy bridging HTTP to gRPC. Whenever it receives an HTTP POST request, it should read the raw body, use the Python gRPC client (generated from your proto) to call the Go gRPC server at `127.0.0.1:50051`, and return the raw gRPC response bytes as the HTTP response with a `200 OK` status.

**5. Execution and Verification**
Start both the Go server and the Python proxy in the background. Ensure they are running.
Once both are running, use `curl` to send an HTTP POST request to `http://127.0.0.1:8080` with the exact raw string payload: `ORBITAL_DATA_STREAM_XYZ`
Save the raw binary response from `curl` to `/home/user/project/result.bin`.

Note: You may need to install standard dependencies via `apt-get` or language package managers if they are not present, but you have the permissions necessary to do so locally in the user directory or via standard unprivileged installs.