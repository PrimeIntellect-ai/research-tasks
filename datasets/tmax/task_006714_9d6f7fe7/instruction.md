You are a developer tasked with fixing and testing a multi-language REST API server. The project is located at `/home/user/project`. 

The project consists of a Rust-based HTTP server that calls a C library via FFI to perform data transformation. Currently, the project is broken in multiple ways:

1. **Rust Compilation Error**: The Rust code in `/home/user/project/src/main.rs` fails to compile due to an incorrect FFI function signature definition for `transform_string`. Fix the signature in `main.rs` so the Rust project compiles successfully.
2. **C Memory Safety Bug**: The C code in `/home/user/project/lib/transform.c` contains a critical memory safety issue (Undefined Behavior). It currently returns a pointer to a local stack array, which results in garbage data or a crash when the Rust code attempts to read and free it. Fix the C code to safely allocate the returned string so that `free_string` can safely deallocate it later.
3. **End-to-End Test Orchestration**: Write a Bash script at `/home/user/project/test_e2e.sh` that orchestrates an end-to-end test of the REST API. The script must:
   - Build and start the Rust server (`cargo run`) in the background.
   - Wait until the server is listening on `127.0.0.1:8080`.
   - Make an HTTP GET request using `curl` to `http://127.0.0.1:8080/api/transform?text=helloworld`.
   - Extract *only* the response body (which should be the transformed text) and write it to `/home/user/project/e2e_result.txt`.
   - Terminate the background Rust server process cleanly.
   - Exit with status code `0`.

Make sure `/home/user/project/test_e2e.sh` has executable permissions (`chmod +x`). 

Do not change the port number or the API endpoint path. You can test your solution by running `./test_e2e.sh` and verifying the contents of `e2e_result.txt`.