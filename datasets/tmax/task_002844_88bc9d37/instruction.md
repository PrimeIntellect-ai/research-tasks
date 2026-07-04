You are a systems programmer working on a Python microservice that uses a native Rust extension for high-performance string processing. The service exposes its functionality via gRPC. 

Recently, we decided to perform a schema migration on our gRPC API to support a `multiplier` parameter, but the transition is incomplete. Furthermore, the Rust extension fails to compile due to a borrow checker/lifetime issue, and our test suite is missing property-based tests.

Your task is to fix the system, update the schema, and write rigorous tests.

Here is the current state of the workspace in `/home/user/project`:
1. `/home/user/project/rust_ext/src/lib.rs` - A PyO3 Rust extension that is supposed to repeat a string `multiplier` times. It currently fails to compile due to a lifetime error.
2. `/home/user/project/proto/service.proto` - The gRPC protobuf schema.
3. `/home/user/project/server.py` - The Python gRPC server implementation.

Complete the following steps:

**Phase 1: Fix the Rust Extension**
1. Fix the ownership and lifetime issues in `/home/user/project/rust_ext/src/lib.rs` so that it successfully compiles and correctly returns the repeated string.
2. Build and install the Python extension in the current environment. (The extension is configured with `maturin` and a `Cargo.toml` is provided in `/home/user/project/rust_ext`).

**Phase 2: Schema Migration & gRPC**
1. Perform a schema migration in `/home/user/project/proto/service.proto`. Add a new field `int32 multiplier = 2;` to the `ProcessRequest` message.
2. Generate the updated Python gRPC and protobuf code into `/home/user/project/`.
3. Update `/home/user/project/server.py` to pass the `multiplier` from the request to the `string_processor.process_string` function. If the multiplier is 0, default to 1.

**Phase 3: Property-based Testing**
1. Create a test file `/home/user/project/test_server.py`.
2. Write a property-based test using `hypothesis` and `pytest`.
3. The test should start a local instance of the gRPC server, connect to it with a client, and use `@given` to generate random strings (`st.text()`) and random multipliers (`st.integers(min_value=1, max_value=10)`).
4. Assert that the length of the returned string exactly equals `len(input_string) * multiplier`.
5. Run your test suite using `pytest /home/user/project/test_server.py -v > /home/user/test_results.log`.

Ensure that the final output file `/home/user/test_results.log` shows that all tests passed successfully.