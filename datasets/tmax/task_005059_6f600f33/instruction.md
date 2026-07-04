You are tasked with fixing a polyglot microservice project located at `/home/user/polyglot_calc`. 
The project consists of a C++ gRPC server that parses and evaluates Reverse Polish Notation (RPN) mathematical expressions, and a Rust client that sends requests to it.

Currently, the project is broken in several ways:
1. **Build Failure:** The C++ server fails to compile because its `CMakeLists.txt` is missing proper linkage for gRPC and Protobuf.
2. **Logic Error:** The C++ RPN evaluator in `cpp_server/evaluator.cc` has a bug where multiplication operations evaluate incorrectly.
3. **Memory Leaks:** The `evaluator.cc` leaks memory heavily during expression evaluation.

Your objectives:
1. Fix `cpp_server/CMakeLists.txt` so the C++ project compiles successfully using CMake.
2. Fix `cpp_server/evaluator.cc` to correctly evaluate RPN expressions (e.g., `3 4 + 5 *` should equal `35`).
3. Eliminate all memory leaks in `cpp_server/evaluator.cc`.
4. Create a bash script `/home/user/polyglot_calc/build_and_test.sh` that:
   - Builds the C++ server using CMake (in `cpp_server/build`).
   - Builds the Rust client using Cargo (in `rust_client`).
   - Starts the C++ gRPC server (`calc_server`) in the background under `valgrind --leak-check=full --log-file=/home/user/valgrind_report.txt`.
   - Waits a few seconds for the server to start.
   - Runs the Rust client (`cargo run --release`), redirecting its standard output to `/home/user/client_output.txt`.
   - Gracefully terminates the C++ server (e.g., using `kill -SIGTERM`) and waits for it to exit so valgrind can write its report.

When you are done, execute `/home/user/polyglot_calc/build_and_test.sh`. 
An automated test will verify that:
- `/home/user/client_output.txt` contains the correct evaluated result from the Rust client's request.
- `/home/user/valgrind_report.txt` shows `0 bytes in 0 blocks` definitely lost.