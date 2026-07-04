You are tasked with fixing a malfunctioning graph traversal utility and building a robust Go-based property testing harness to verify its correctness and performance. 

There are two main components in your `/home/user/workspace` directory:
1. A Rust project in `/home/user/workspace/rust_graph` that is supposed to perform dependency resolution (topological sorting) on directed acyclic graphs (DAGs). However, the original developer left it in a broken state. It currently fails to compile due to Rust ownership and borrow checker errors in `src/resolver.rs`.
2. A Go project skeleton in `/home/user/workspace/go_tester`.

Your objectives are:
1. **Fix the Rust Project:** Debug and fix the borrow checker and ownership errors in `/home/user/workspace/rust_graph/src/resolver.rs` without changing the underlying traversal algorithm's logic.
2. **Cross-Compilation:** Configure the Rust project to cross-compile to `x86_64-unknown-linux-musl` and build the release binary. Place the compiled binary exactly at `/home/user/workspace/rust_graph/bin/graph_resolver`.
3. **Write a Go Property Tester:** Write a Go testing harness in `/home/user/workspace/go_tester/bench_test.go`. We have provided a black-box, stripped binary oracle at `/app/oracle_graph_solver` which perfectly implements the graph traversal specification.
   - Your Go code must use property-based testing (via `testing/quick` or a similar standard library approach) to generate at least 5,000 random DAG dependency lists.
   - For each generated graph, invoke both the compiled `/home/user/workspace/rust_graph/bin/graph_resolver` and the `/app/oracle_graph_solver`.
   - Assert that both binaries produce the exact same topological sort order (or both return a cycle error).
   - The Go tester must run as a Go Benchmark (`BenchmarkGraphSolver`).
4. **Performance Tuning:** The Go test harness must evaluate the generated graphs concurrently. The testing throughput must exceed a specific metric threshold (at least 500 test executions per second) to pass our CI verifier.

Format requirements:
- The Rust binaries and the oracle binary take a single argument: a string representing the graph (e.g., `"A->B, B->C, A->C"`).
- They output the sorted nodes comma-separated (e.g., `"A,B,C"`) or `"CYCLE_DETECTED"` to stdout.
- Ensure your Go benchmark is written so that `go test -bench .` outputs the standard Go benchmark format showing `ops/sec`.

You must leave the final working Go harness in `/home/user/workspace/go_tester/bench_test.go` and the compiled Rust binary in `/home/user/workspace/rust_graph/bin/graph_resolver`. Do not modify the oracle binary.