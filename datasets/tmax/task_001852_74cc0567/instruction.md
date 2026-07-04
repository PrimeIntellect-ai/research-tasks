You are a systems programmer working on a Rust wrapper for a legacy C library, `libexpr`. This library parses and evaluates mathematical expressions, but it has severe memory safety vulnerabilities (e.g., stack overflows on deep recursion, uncontrolled pointer arithmetic on specific syntax). 

Your team has decided to put a Rust-based sanitizer in front of it rather than rewriting the C library immediately. 

Currently, the Rust FFI wrapper project in `/home/user/expr_ffi` is broken:
1. The build script (`/home/user/expr_ffi/build.rs`) is failing to correctly compile and statically link `libexpr.c`. It mimics a broken package configuration.
2. The sanitizer logic in `/home/user/expr_ffi/src/sanitizer.rs` is incomplete. 

Your tasks:
1. **Fix the build issue:** Repair `/home/user/expr_ffi/build.rs` so that `cargo build` correctly compiles `src/libexpr.c` and links it statically as `expr_c` to the Rust project.
2. **Design a Custom AST / Parsing Data Structure:** Implement the `is_safe_expression` function in `/home/user/expr_ffi/src/sanitizer.rs`. It must parse basic arithmetic expressions (digits, `+`, `-`, `*`, `/`, `(`, `)`) and return `true` if it is safe, and `false` if it is malicious. 
3. **Prevent Malicious Inputs:** The C library crashes if:
   - The expression nesting level (parentheses) exceeds 15.
   - A division by zero is syntactically present (e.g., `... / 0` or `... / (0)`).
   - There are sequential operators without operands (e.g., `1 ++ 2`).
4. **Build a CLI Tool:** Ensure the provided `/home/user/expr_ffi/src/main.rs` is functional. It reads a file path from the command line, runs your sanitizer, and exits with `0` if the expression is clean, or `1` if it is malicious.
5. **CI/CD Pipeline:** Create a shell script `/home/user/expr_ffi/ci_check.sh` that builds the project in release mode and iterates over all files in `/app/corpora/clean/` and `/app/corpora/evil/`, executing the CLI tool on each. It should print `PASS` or `FAIL` for each file and exit with code 0 only if 100% of the tests pass.

*Hints:*
- A stripped, legacy binary of an older, safer parser is available at `/app/reference_oracle`. You can feed it text files to see how a correct parser evaluates boundary conditions (`/app/reference_oracle <file>`).
- You may use standard Rust libraries for parsing, but you must define your own logical validation rules to classify the strings.