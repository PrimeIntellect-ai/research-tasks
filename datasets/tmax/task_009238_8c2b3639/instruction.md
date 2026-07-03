You are an open-source maintainer reviewing a Pull Request that attempts to refactor a monolithic Rust application into a gRPC client-server architecture. Unfortunately, the contributor left the PR in a broken state. 

Your task is to fix the repository located at `/home/user/grpc_refactor_pr`.

Here is the current situation:
1. **Circular Dependency:** The contributor accidentally created a circular dependency in the Cargo workspace. The `client` crate depends on the `server` crate to access the generated protobuf bindings, and the `server` crate depends on the `client` crate to access a shared `AppConfig` struct. 
2. **Broken Protobuf:** The gRPC service definition at `server/proto/service.proto` has a syntax error that prevents `tonic-build` from compiling.
3. **Incomplete JSON Parsing:** The client is supposed to read a structured JSON file, transform it into the gRPC request type, and send it. The parsing logic in `client/src/main.rs` is incomplete.
4. **Failing CI/CD:** The GitHub Actions workflow file at `/home/user/grpc_refactor_pr/.github/workflows/rust.yml` has syntax and command errors.

**Your Objectives:**
1. **Refactor the Workspace:** Create a new library crate named `common` in the workspace. Move the protobuf definitions, `tonic-build` logic, and the `AppConfig` struct into this `common` crate. Update the `client` and `server` crates to depend on `common` instead of each other, completely resolving the circular dependency. 
2. **Fix the Protobuf:** Correct the syntax errors in `service.proto`.
3. **Fix the CI/CD Pipeline:** Correct the errors in `.github/workflows/rust.yml` so it runs `cargo fmt --check`, `cargo test`, and `cargo build --release` correctly.
4. **Complete the Client:** Fix `client/src/main.rs` so it successfully parses `/home/user/grpc_refactor_pr/input.json` using `serde_json`, constructs the gRPC request, and prints the server's response to standard output.
5. **Verification:** 
   - Start the gRPC server in the background.
   - Run the client, reading `/home/user/grpc_refactor_pr/input.json`.
   - Save the exact standard output of the client to `/home/user/verification.log`.

The workspace must compile cleanly with `cargo build --workspace`.