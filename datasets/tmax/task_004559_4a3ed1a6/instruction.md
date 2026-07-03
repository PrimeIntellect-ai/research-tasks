I am migrating an old Python 2 web backend script that insecurely used `eval()` to calculate user-provided math expressions, which poses a severe web security risk. I want to migrate to Python 3 and replace the insecure `eval()` call with a secure parser written in Rust, communicating via FFI.

Please perform the following steps:

1. Create a Rust library named `safe_eval` in `/home/user/calculator/safe_eval` (use `cargo new --lib safe_eval`). Configure its `Cargo.toml` to compile as a `cdylib`.
2. In the Rust library, implement a function exported to C with the exact signature: `int32_t evaluate_expr(const char* expr)`. 
   - The function should take a valid null-terminated C string representing a math expression.
   - Expressions will only contain positive integers, `+` operators, `-` operators, and spaces (e.g., `"10 + 5 - 2"`). Assume all inputs are perfectly formatted with spaces separating operators and operands.
   - The function must parse the string, evaluate the expression left-to-right, and return the `i32` result.
3. Build the Rust library in release mode.
4. Write a Python 3 script at `/home/user/calculator/secure.py` that:
   - Uses the `ctypes` module to load the compiled Rust shared object from `/home/user/calculator/safe_eval/target/release/libsafe_eval.so`.
   - Reads each line from `/home/user/calculator/input.txt`.
   - Passes the string to the Rust `evaluate_expr` function (make sure to encode the Python string to bytes so it passes as a valid C string pointer).
   - Writes the returned integer result to `/home/user/calculator/secure_output.txt`, one result per line in the exact order of the inputs.
5. Run your Python script so that `secure_output.txt` is generated.