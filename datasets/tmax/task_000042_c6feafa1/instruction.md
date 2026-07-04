You are a platform engineer maintaining the CI/CD pipeline for a large microservices platform. Recently, a critical CI step that runs a custom web security audit tool (`route-auth-auditor`) has been timing out on a specific API Gateway configuration. Additionally, a recent change broke one of the URL decoding unit tests.

The `route-auth-auditor` tool is a Rust application vendored at `/app/route-auth-auditor`. It simulates inbound requests, parses their URL parameters, evaluates authorization expressions, and traverses the dependency graph of internal service routes to ensure sensitive endpoints are protected.

Your task is to fix the vendored package so that it is both functionally correct and performant:
1. Fix the URL parameter decoding logic in `/app/route-auth-auditor/src/decoder.rs`. Currently, it fails to properly decode standard percent-encoded characters (e.g., `%20`, `%2B`). You must make the existing failing unit test (`cargo test`) pass.
2. The CI timeout is caused by a performance issue in `/app/route-auth-auditor/src/graph.rs`. The tool evaluates the authorization graph recursively, which leads to exponential time complexity on highly interconnected DAGs (diamond dependencies). Refactor the graph traversal logic to use memoization (or another O(N) strategy) so that nodes are only evaluated once. 
3. Verify your performance fix by running the tool against a large generated test fixture located at `/app/test_data/large_gateway.json`.
4. Compile your fixed version using `cargo build --release` and copy the resulting executable to `/home/user/auditor_bin`.

The automated verifier will:
- Check that `cargo test` passes in `/app/route-auth-auditor`.
- Run `/home/user/auditor_bin /app/test_data/large_gateway.json` and measure its execution time. The execution time must be strictly less than 0.25 seconds.