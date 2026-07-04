You are a developer organizing project files by building a custom file-processing daemon in Rust. 

You have been provided with a starter workspace in `/home/user/file_manager`. However, it is incomplete, has a memory leak, and fails to build due to linking errors.

Your objectives:
1. **Build System & Linking**: The project depends on a custom C library located in `/home/user/file_manager/clib` (contains `checksum.c` and `checksum.h`). You must compile this C file into a static library (`libchecksum.a`) and configure `Cargo.toml` and `build.rs` to statically link it to the Rust project. The Rust FFI bindings are already declared in `src/main.rs`.
2. **Expression Evaluation**: Implement the `evaluate_rpn` function in `src/main.rs`. It must evaluate a Reverse Polish Notation (RPN) string. Supported tokens are integer numbers, `SIZE` (which substitutes the file size), `+`, `-`, `*`, and `>`. The function should return `1` if the expression evaluates to true (or a positive number > 0), and `0` otherwise.
3. **Request Validation & Rate Limiting**: The system processes a list of file operation requests from `/home/user/requests.csv` (format: `timestamp_ms,filename,file_size,rpn_expr`). Implement a rate limiter: any request arriving strictly less than `200ms` after the *last accepted request* must be dropped (ignored). The first request is always checked.
4. **Memory Debugging**: The starter code in `src/main.rs` contains an intentional memory leak in the `process_filename` function (it allocates a CString and forgets/leaks it). Fix this memory leak so the program runs clean under Valgrind (or simply frees the memory correctly).
5. **Execution**: Run the compiled tool. For every accepted request where the RPN expression evaluates to > 0, write a line to `/home/user/organizer.log` in the format:
   `[timestamp_ms] ACCEPTED filename checksum_result`
   *(The `checksum_result` is obtained by calling the linked C function `compute_checksum(filename)`)*

You must produce the final `/home/user/organizer.log` file. All tools (Cargo, Rustc, GCC) are available.