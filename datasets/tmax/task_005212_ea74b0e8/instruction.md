You are tasked with fixing a multi-file Rust project located in `/home/user/rust_app` that currently fails to compile. The project relies on a generated configuration file that must be dynamically created by a custom C++ tool, which you need to write.

**Phase 1: Write the C++ Configuration Generator**
Create a C++ program at `/home/user/rust_app/generator.cpp`. This tool must perform the following tasks:
1. **Expression Parsing and Evaluation**: Read a file named `/home/user/rust_app/config.expr`. This file contains variable definitions with arithmetic expressions.
   - Format: `DEF <VAR_NAME> = <EXPRESSION>`
   - Expressions will contain integers, the operators `+`, `-`, `*`, `/`, parentheses `()`, and previously defined variable names.
   - You must parse and evaluate these expressions using standard integer arithmetic. You will need to build a custom parser/evaluator (e.g., using a state machine, recursive descent, or Shunting-yard algorithm).
2. **Code Generation**: Output a valid Rust file at `/home/user/rust_app/src/generated_config.rs`.
   - Format for each variable: `pub const <VAR_NAME>: i32 = <EVALUATED_VALUE>;`
   - The variables in the Rust file **must be sorted alphabetically** by their variable names.
3. **Sorting, Merging, and Diffing**: Read an older configuration state from `/home/user/rust_app/previous_config.txt`.
   - Format: `<VAR_NAME>=<VALUE>`
   - Compare the newly evaluated variables against this previous state.
   - Output a diff file at `/home/user/rust_app/config_diff.txt`.
   - The diff should contain **only** modified or newly added variables.
   - For newly added variables, format as: `+ <VAR_NAME>=<NEW_VALUE>`
   - For modified variables, format as: `~ <VAR_NAME>=<OLD_VALUE>-><NEW_VALUE>`
   - The lines in `config_diff.txt` **must be sorted alphabetically** by variable name.

**Phase 2: CI/CD Pipeline Setup**
Create a Bash script at `/home/user/rust_app/ci_pipeline.sh` that acts as a simple CI pipeline. The script must:
1. Compile the C++ program `generator.cpp` using `g++` into an executable named `generator` (using standard C++17).
2. Execute the `generator` executable.
3. Compile the Rust project using `cargo build` in the `/home/user/rust_app` directory.
4. Exit with a non-zero code if any step fails, and `0` on total success.
5. Ensure the script is executable.

You must write the C++ code, write the Bash script, and run the Bash script to successfully build the Rust project and generate the `config_diff.txt`. Assume `g++` and `cargo` are already installed and available in the environment.