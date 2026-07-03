You are an engineer tasked with porting a Linux monitoring tool to work in a minimal container environment. 
The Rust project is located in `/home/user/monitor_workspace`. It is a Cargo workspace containing two crates: `api` and `core`.

Currently, the workspace fails to compile due to a circular dependency. The `core` crate depends on `api` to use the `UptimeResponse` struct, and the `api` crate depends on `core` to call system monitoring functions. 

Your objectives:
1. **Fix the Circular Dependency**: Refactor the crates so that the workspace compiles successfully. You can move the `UptimeResponse` struct into `core` and remove the dependency of `core` on `api`.
2. **Implement Minimal Container Support**: The function `read_uptime` in `core/src/lib.rs` currently hardcodes the path `"/proc/uptime"`. Modify it to accept a base `proc_dir` (e.g., `read_uptime(proc_dir: &str)`) so it can be tested or run in different environments. It must read the file `{proc_dir}/uptime` and parse the first space-separated value as an `f64`.
3. **Setup Test Fixtures**: Create a mock directory at `/home/user/mock_proc` containing a file named `uptime`. The file must contain exactly `12345.67 890.12`.
4. **Integration Testing**: Update the `api` crate's endpoints and tests. Ensure `api` exposes a function to handle a GET request returning JSON `{"uptime": <value>}`. Write an integration test in `api/src/lib.rs` or `api/tests/` that uses your mock `/home/user/mock_proc` directory, calls the function/endpoint, and asserts that the returned uptime value is `12345.67`.
5. **Validation**: Once everything compiles and tests pass, run `cargo test --workspace > /home/user/test_results.txt` to save the test output.

Ensure the final project builds cleanly with `cargo build` and all tests pass with `cargo test`.