You are an engineer tasked with setting up a polyglot test pipeline from scratch for a project containing C and Rust components. The project is located at `/home/user/polyglot_project`. 

Currently, the build and tests are failing due to two issues:
1. `worker.c` contains undefined behavior (an out-of-bounds array access).
2. `parser.rs` fails to compile due to a Rust borrow checker error (violating mutable and immutable borrowing rules).

Your objectives are to:
1. Create a single, valid unified diff patch file named `/home/user/polyglot_project/fixes.patch` that fixes both `worker.c` and `parser.rs`.
    - `worker.c` should be fixed so that it iterates exactly over the 5 initialized elements of the array, calculating the sum (`1 + 2 + 3 + 4 + 5 = 15`). It should print `Sum: 15`.
    - `parser.rs` should be fixed to print `Read: hello` and then `Write: hello world` without triggering a borrow checker error. The variable `s` must be appended with `" world"`.
2. Write a Python test orchestrator script at `/home/user/polyglot_project/orchestrator.py` that performs the following steps programmatically:
    - Uses Python's `subprocess` module to apply `fixes.patch` using the `patch` command (e.g., `patch -p1 < fixes.patch` or similar, depending on how you structure your diff).
    - Compiles `worker.c` into an executable named `worker` using `gcc`.
    - Compiles `parser.rs` into an executable named `parser` using `rustc`.
    - Executes the existing `/home/user/polyglot_project/e2e_test.py` script.
    - Captures the standard output of `e2e_test.py` and writes it exactly as-is to `/home/user/polyglot_project/success.log`.

Run your `orchestrator.py` script to ensure it creates `success.log` successfully with the passing test output. 

*Note: Ensure your patch paths align with the directory structure you are executing from.*