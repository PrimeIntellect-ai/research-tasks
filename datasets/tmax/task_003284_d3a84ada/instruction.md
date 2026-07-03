I need you to fix and complete a polyglot project analyzer tool. The tool is designed to organize project files by parsing them, finding their dependencies (via `include "..."` statements), and outputting a topologically sorted list of files. 

The project consists of two parts:
1. A C library called `libfastdir` vendored at `/app/libfastdir`. It handles the fast file reading and extraction of dependency statements.
2. A Rust CLI called `analyzer` located at `/home/user/analyzer`. It uses the C library via FFI, builds a dependency graph, and performs the topological sort.

However, the project is currently broken:
- The `Makefile` in `/app/libfastdir` has some errors. It fails to compile the static library `libfastdir.a` because of missing compiler flags (it needs `-fPIC`) and a broken clean rule.
- The Rust project at `/home/user/analyzer` has a `build.rs` file that fails to link the C library correctly because it's looking in the wrong directory.
- The Rust source code (`src/main.rs` and `src/graph.rs`) contains ownership and borrow-checker errors related to how it inserts nodes into the graph and traverses them. 

Your tasks:
1. Fix the `Makefile` in `/app/libfastdir` and compile `libfastdir.a`.
2. Fix `/home/user/analyzer/build.rs` to correctly link the compiled C library.
3. Fix the borrow checker and lifetime issues in the Rust code so that it compiles successfully. The topological sort must correctly resolve the graph dependencies. If there is a circular dependency, the program must print "CYCLE DETECTED" to stdout and exit with code 0.
4. Build the release version of the Rust CLI.

The final executable must be located at `/home/user/analyzer/target/release/analyzer`. It should accept a single command-line argument (a directory path) and print the topologically sorted filenames (one per line) to standard output.