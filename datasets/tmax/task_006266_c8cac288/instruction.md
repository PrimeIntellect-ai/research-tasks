You are tasked with setting up a polyglot build system for a new Web Application Firewall (WAF). The system relies on a C++ core for fast packet processing and a Rust library for memory-safe HTML sanitization (to prevent XSS attacks). 

Currently, the build system is broken in two ways:
1. The dependency resolution script is incomplete.
2. The Rust sanitization library fails to compile due to a strict ownership/borrow checker issue.

Your objectives:

1. **Graph Traversal for Dependency Resolution (C++)**
   There is a skeleton C++ file at `/home/user/project/resolver.cpp`. It parses a simple dependency graph from `/home/user/project/deps.txt`. You must implement the topological sorting logic (e.g., using DFS or Kahn's algorithm) inside `resolver.cpp` to determine the correct build order. 
   Compile and run your C++ program so that it writes the correct build order (space-separated target names, from independent to most dependent) into `/home/user/project/build_order.txt`.

2. **Fix the Rust Borrow Checker Issue**
   The Rust crate is located at `/home/user/project/rust_sanitizer/`. It currently fails to build due to a borrow checker error in `src/lib.rs`. Identify the ownership/borrowing conflict, fix the code so it compiles without warnings or errors, and preserves the functional intent (appending " [sanitized]" to the input string and returning it).

3. **Build the Rust Library**
   Once fixed, build the Rust crate using Cargo in release mode so that the static library is produced.

Expected final state for verification:
- `/home/user/project/build_order.txt` contains the correct, topologically sorted build order.
- The Rust library compiles successfully and its release artifact exists at `/home/user/project/rust_sanitizer/target/release/librust_sanitizer.rlib`.