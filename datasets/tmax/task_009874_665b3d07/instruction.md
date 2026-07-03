You are tasked with porting a core mathematical parsing tool to a minimal environment. The system will consist of a high-performance Rust library for mathematical evaluation and a lightweight C frontend that loads this library dynamically.

Your objective is to build this system from scratch, manage the shared library and application binary interface (ABI), and orchestrate the build and end-to-end testing with a shell script.

Here are the requirements:

1. **Rust Shared Library (`/home/user/rpn_calc`)**
   - Create a new Rust project in `/home/user/rpn_calc`.
   - Configure `Cargo.toml` so the crate compiles as a dynamic C-compatible shared library (`cdylib`). The output library should be named `librpn_calc.so`.
   - In `src/lib.rs`, implement a Reverse Polish Notation (RPN) expression parser and evaluator for 64-bit floating point numbers (`f64`). 
   - Supported operators must include: `+`, `-`, `*`, `/`.
   - Operands and operators in the input string will be strictly separated by single spaces.
   - Expose exactly one C-compatible ABI function: 
     `#[no_mangle] pub extern "C" fn eval_rpn(expr: *const std::os::raw::c_char) -> f64`
   - If the expression is invalid, unbalanced, or division by zero occurs in a way that results in an invalid state, you may return `f64::NAN`, though the test expressions will be well-formed.

2. **C Frontend (`/home/user/frontend.c`)**
   - Write a C program that takes exactly one command-line argument (the RPN expression string).
   - Use `dlopen` and `dlsym` to dynamically load `librpn_calc.so` from the current working directory (`./librpn_calc.so`) and extract the `eval_rpn` function pointer.
   - Call the loaded function with the provided argument.
   - Print the evaluated result to standard output using the format `"%.2f\n"`.
   - If `dlopen` or `dlsym` fails, the program should print an error message and exit with a non-zero code.

3. **End-to-End Orchestration Script (`/home/user/run_e2e.sh`)**
   - Write a bash script that fully automates the build and test process.
   - The script must build the Rust library in release mode.
   - Copy the compiled `librpn_calc.so` from the Rust target directory to `/home/user/`.
   - Compile the C frontend using `gcc frontend.c -o frontend -ldl`.
   - Execute the compiled C program with the exact mathematical expression: `"15 7 1 1 + - / 3 * 2 1 1 + + -"`
   - Save the standard output of the execution strictly to `/home/user/e2e_output.txt`.

Ensure your bash script is executable (`chmod +x`). Once you have written everything, run `/home/user/run_e2e.sh` so the library is compiled and the `e2e_output.txt` file is generated.