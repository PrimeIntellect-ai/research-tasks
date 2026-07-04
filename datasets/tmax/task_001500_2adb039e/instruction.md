You are a web developer building a backend worker for a real-time math evaluation feature. To maintain performance and compatibility with legacy systems, the actual math parsing and evaluation is done in a C library, but the worker logic must be written in Rust.

You have been provided with a C source file at `/home/user/calc.c` that contains a function:
`double evaluate_addition(const char* expr);`
This function takes a string containing an addition expression (e.g., "5 + 10") and returns the computed result as a double.

Your task is to:
1. Compile the `/home/user/calc.c` file into a shared library named `libcalc.so` in `/home/user`.
2. Write a Rust program at `/home/user/processor.rs` that reads incoming requests from `/home/user/requests.txt`.
3. In your Rust program, use FFI to link against `libcalc.so` and call `evaluate_addition` to calculate the result of the expressions.
4. Implement **Request Validation**: Before evaluating, your Rust program must skip any lines that start with a `#` character, and skip any lines that are strictly longer than 15 characters.
5. Implement **Rate Limiting**: Your program should only evaluate a maximum of 3 valid requests. Once 3 valid expressions have been evaluated, stop processing the file.
6. Write the successful evaluations to `/home/user/results.log`. Each line should be formatted exactly as `<original_line> = <result>`, where the result is formatted to exactly 1 decimal place (e.g., "1 + 1 = 2.0").
7. Compile and execute your Rust program so that `results.log` is generated.

Constraints:
- You must use `rustc` directly to compile your Rust code (no Cargo project is needed).
- Make sure to handle the C string conversion properly in your Rust FFI boundary.
- Do not modify `/home/user/calc.c` or `/home/user/requests.txt`.