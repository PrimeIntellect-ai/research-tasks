You are tasked with fixing and integrating a multi-service data processing pipeline located at `/app`. The system consists of three services:
1. A Redis cache.
2. A legacy Expression Engine (Python) that translates abstract rule IDs into Abstract Syntax Trees (ASTs) representing semantic version constraints.
3. A Rust API (`rust-processor`) that receives requests, fetches the AST from the Expression Engine, evaluates the semantic version constraints against a provided version, and caches the result.

Currently, the `rust-processor` project fails to compile, is missing key implementations, and the services are not wired up properly. 

Your objectives are:
1. **Patch Application:** Apply the patch file located at `/app/patches/redis-support.patch` to the `/app/rust-processor` repository. This patch introduces Redis caching but introduces compilation errors due to missing imports and a minor type mismatch in `src/cache.rs`. Fix these compilation errors.
2. **Semantic Version Evaluation:** In `src/evaluator.rs`, implement the missing `evaluate_semver_ast` function. It receives a translated AST from the Python service (parsed as a JSON struct) and must evaluate a given semantic version string against it. The AST supports `AND`, `OR`, and `CONSTRAINT` node types. You must implement the logic to correctly parse and compare standard semantic versions (e.g., `>=1.2.0`, `<2.0.0`).
3. **Test Fixtures:** The test suite in `/app/rust-processor/tests/integration_test.rs` is failing because it expects a mock fixture file at `/app/rust-processor/tests/fixtures/mock_ast.json`. Create this file to represent a valid AST JSON structure that evaluates to `true` for version `1.4.5`.
4. **Integration & Startup:** Ensure all `rust-processor` tests pass (`cargo test`). Once the code compiles and tests pass, start all three services in the background:
   - Start `redis-server` on its default port (`6379`).
   - Start the legacy engine by running `python3 /app/legacy-engine/app.py` (listens on `127.0.0.1:8081`).
   - Run the Rust processor via `cargo run --release` in `/app/rust-processor` (listens on `127.0.0.1:8080`).

The Rust processor's `server.rs` uses environment variables `REDIS_URL` and `LEGACY_ENGINE_URL`. You must start the Rust processor with `REDIS_URL=redis://127.0.0.1:6379` and `LEGACY_ENGINE_URL=http://127.0.0.1:8081`.

The verifier will send HTTP POST requests to the Rust processor at `http://127.0.0.1:8080/evaluate`. The expected JSON payload format is: `{"version": "1.4.5", "rule_id": "beta-testing"}`. The Rust processor must return `{"allowed": true}` or `{"allowed": false}`.