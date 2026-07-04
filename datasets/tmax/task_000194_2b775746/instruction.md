You are a build engineer at a data processing company. We are migrating our schema management and artifact dependency resolution system from a legacy C-based toolchain to a new Rust-based microservice.

Currently, we have two main problems:
1. Our new Rust project at `/home/user/workspace/migration-service` fails to compile due to several complex lifetime and borrow-checker issues in the `graph_parser` and `schema_loader` modules.
2. The core dependency resolution logic (which takes a list of artifacts/migrations and their dependencies and outputs a strictly ordered build sequence) is missing from the Rust project. We lost the source code for the legacy resolver. All we have is the stripped, dynamically linked binary located at `/app/legacy_graph_resolver`.

Your task is to:
1. Fix the Rust compilation errors in `/home/user/workspace/migration-service` without changing the publicly exposed function signatures. The project includes a REST API (using `axum`) that handles artifact dependency submissions.
2. Analyze `/app/legacy_graph_resolver`. This binary takes input from `stdin` in a specific plain-text format: a line with the number of nodes `N`, followed by `N` lines of node names, a line with the number of directed edges `E`, and `E` lines of `Source Destination` pairs indicating `Source` must be built before `Destination`. It outputs a comma-separated list of nodes in the exact order they should be built. You need to reverse-engineer its graph traversal and topological sorting algorithm, paying specific attention to how it breaks ties when multiple nodes have an in-degree of 0.
3. Implement this exact bit-equivalent sorting algorithm in the Rust project.
4. Provide a standalone CLI wrapper for your implementation at `/home/user/workspace/migration-service/src/bin/agent_resolver.rs` that reads from `stdin` and writes to `stdout` in the exact same format as the legacy binary. Ensure it builds to `/home/user/workspace/migration-service/target/release/agent_resolver`.
5. Integrate the logic into the `axum` REST API so that a POST request to `/api/v1/resolve` containing a JSON representation of the graph returns the ordered sequence. 

An automated fuzzer will run thousands of randomly generated dependency graphs against both `/app/legacy_graph_resolver` and `/home/user/workspace/migration-service/target/release/agent_resolver` to verify bit-exact output equivalence.