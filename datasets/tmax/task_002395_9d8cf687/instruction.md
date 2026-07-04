You are tasked with fixing a secure utility designed to parse and evaluate mathematical expressions for a web application backend. For security and memory-safety reasons, the expression evaluator is written in Rust, while the server wrapper that handles web input is written in C.

Currently, the project is broken. The original script developer left behind several issues:
1. The Rust parsing library has an ownership and borrow checker error and fails to compile.
2. The C program references the wrong FFI function name.
3. The `Makefile` is incomplete and fails to build the Rust library or link it to the C program correctly.

Your goal is to fix these components, successfully compile the project, and test it.

**Workspace details:**
- Project directory: `/home/user/web_eval`
- Rust library path: `/home/user/web_eval/parser` (contains `Cargo.toml` and `src/lib.rs`)
- C server path: `/home/user/web_eval/server.c`
- Makefile path: `/home/user/web_eval/Makefile`

**Objectives:**
1. Fix the Rust borrow checker error in `/home/user/web_eval/parser/src/lib.rs`. The code attempts to instantiate an `Evaluator` struct but mismanages the lifetime of a local `String`. You must fix the logic so it correctly tokenizes and evaluates the expression without memory issues.
2. Fix `/home/user/web_eval/server.c` to properly declare and call the exported Rust function.
3. Update the `Makefile` so that running `make` will:
   - Build the Rust project in release mode (`cargo build --release` inside the `parser` directory).
   - Compile `server.c` into an executable named `server` in the `/home/user/web_eval` directory, properly linking the compiled static Rust library (`libparser.a`) and any necessary system libraries (like `pthread`, `dl`, `m`).
4. Once the build succeeds, run the utility with a specific Reverse Polish Notation (RPN) expression to verify it works.

**Verification:**
Execute the compiled server program with the argument `"5 1 2 + 4 * + 3 -"` and redirect standard output to a log file.
```bash
./server "5 1 2 + 4 * + 3 -" > /home/user/web_eval/output.log
```
The automated test will verify the presence and content of `/home/user/web_eval/output.log`.