You are a web developer integrating a new feature backend for our microservices architecture. We have a Rust-based gRPC server for the new feature and a C++ integration test client. Unfortunately, our build configuration is broken (similar to a broken `setup.py` but for CMake) and someone committed Rust code that doesn't compile due to ownership issues.

Your task is to fix the build systems, fix the code, run the tests, and produce a verification log.

The project is located at `/home/user/project/`. It contains:
1. `proto/feature.proto`: The gRPC protobuf definition.
2. `backend_rust/`: A Rust `tonic` gRPC server.
3. `client_cpp/`: A C++ client that tests the feature.

Here is what you need to do:

1. **Fix the Rust Server:** 
   Navigate to `/home/user/project/backend_rust/`. The server has a borrow checker/ownership error in `src/main.rs`. Find and fix the error so that the server compiles successfully using `cargo build`. Run the server in the background (it binds to `127.0.0.1:50051`).

2. **Fix the C++ Client Build:**
   Navigate to `/home/user/project/client_cpp/`. The `CMakeLists.txt` is incomplete. It fails to properly link the gRPC and Protobuf libraries to the `feature_test` executable. Fix the `CMakeLists.txt` so that it successfully configures and compiles using:
   ```bash
   mkdir build && cd build
   cmake ..
   make
   ```

3. **Run the Integration Test:**
   The compiled C++ client (`feature_test`) takes an ID as a command-line argument, calls the Rust gRPC server, and prints the response.
   Execute the C++ client with the ID `778899`.
   Capture the exact standard output of the C++ client into a log file at `/home/user/project/test_results.log`.

Do not change the gRPC protobuf definitions or the port (`50051`) the server uses. The final success state is defined by the correct generation of `/home/user/project/test_results.log` containing the server's response.