I am trying to organize a large repository of project configuration files (manifests), but I suspect some of them contain malicious embedded bytecode scripts. I am building a custom linter in Rust to filter them out, but I'm completely stuck on a few issues.

I have a multi-file Rust project at `/home/user/rust_linter`. It's designed to read JSON project manifests, deserialize them, and evaluate an embedded bytecode string to classify if a manifest is `clean` or `evil`. 

To do this, it relies on a small C library that emulates the bytecode execution, which is located in `/home/user/rust_linter/c_src/`. However, my project is currently broken in two ways:
1. The Makefile in `c_src/` is broken and fails to compile `libvm.a`. It has some syntax or compilation flag errors.
2. The Rust code in `src/` fails to compile due to several lifetime and borrow checker issues when parsing the JSON data and passing references to the C FFI.

I need you to:
1. Fix the Makefile in `c_src/` so it correctly produces a static library (`libvm.a`) that can be linked by Rust.
2. Fix the lifetime errors in the Rust codebase without changing the core classification logic. 
3. Build the final executable using `cargo build --release`. 

The compiled executable must be located at `/home/user/rust_linter/target/release/rust_linter`. It should take a single file path as a command-line argument. It must read the JSON file, extract the bytecode, evaluate it using the C VM via FFI, and exit with status code `0` if the file is clean, or exit code `1` if the file is evil.

You are provided with a reference implementation of the validator as a stripped binary at `/app/legacy_validator`. You can use this to understand the classification behavior if needed, or to verify your own linter's output on test files.

There are test corpora available in `/home/user/corpora/clean/` and `/home/user/corpora/evil/` which you can use to test your program. A completely successful solution will perfectly reject the evil files and accept the clean files.