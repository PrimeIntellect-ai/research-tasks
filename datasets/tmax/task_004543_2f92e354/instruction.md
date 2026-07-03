You are a script developer tasked with creating a CI/CD build utility in Bash. 

In the directory `/home/user/project`, there is a hybrid C and Rust project that parses and evaluates basic mathematical expressions. The project structure is:
- `/home/user/project/c_src/ops.c`: Contains a C function `multiply(int a, int b)`.
- `/home/user/project/rust_src/main.rs`: A Rust program that parses a hardcoded expression ("10 + 20 * 3"), calls the C `multiply` function via FFI, and adds the result.

However, the build is currently broken:
1. The Rust code fails to compile due to a strict ownership/borrow checker error in `main.rs` (a value is moved and then borrowed).
2. The shared library compilation and linking step is missing.

Your task is to write a Bash script at `/home/user/fix_and_build.sh` that automates the following pipeline:
1. Create a directory `/home/user/project/lib`.
2. Compile `/home/user/project/c_src/ops.c` into a shared library named `libmathops.so` inside `/home/user/project/lib`.
3. Fix the borrow checker error in `/home/user/project/rust_src/main.rs` programmatically within your bash script (e.g., using `sed` or similar standard utilities). The error is located in the `main` function where `expr` is moved to `s` but then borrowed by `parse_and_calc`.
4. Compile the Rust program `main.rs` into an executable named `calc_app` in `/home/user/project/`, ensuring it correctly links against `libmathops.so` and sets the appropriate rpath or linker arguments so the binary can find the shared library at runtime without modifying global system state.
5. Execute `calc_app` and redirect its standard output to `/home/user/result.txt`.

Requirements:
- Ensure the Bash script is executable (`chmod +x`).
- Do not modify the source files manually; your Bash script must perform all fixes and builds when run.
- You must run your script to ensure `/home/user/result.txt` is generated successfully before completing the task.