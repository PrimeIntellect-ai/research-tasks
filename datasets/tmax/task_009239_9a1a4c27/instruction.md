I have a directory of interdependent configuration files at `/home/user/configs`. Each file represents a variable, and its value is determined by a simple arithmetic expression. Some expressions refer to the values of other files in the same directory. 

I need you to write a Go program at `/home/user/evaluator.go` that parses these files, resolves their dependencies, and evaluates the final integer value for each file.

Here are the rules for the configuration files:
1. Each file contains exactly one line.
2. The line contains either a single integer (e.g., `42`) OR a binary operation with operands and an operator separated by a single space (e.g., `B.txt + 5` or `10 * 2`).
3. An operand can be either a direct integer or the exact filename of another configuration file in `/home/user/configs` (which means you must resolve that file's value first).
4. The supported operators are `+`, `-`, `*`, and `/`.
5. There are no circular dependencies.

Additional constraints and requirements:
- **C Interoperability (cgo):** I have provided a C library in `/home/user/math_ops.c` and `/home/user/math_ops.h` containing a function `int evaluate_op(int a, int b, char op);`. **You MUST use this C function via `cgo`** to perform any arithmetic operations (`+`, `-`, `*`, `/`). Do not perform the math directly in Go.
- **Concurrency:** Use Go goroutines and channels to read the contents of the files from the disk concurrently before starting the evaluation phase.
- **Output:** After computing the final value for all files, your Go program must write the results to a JSON file at `/home/user/results.json`. The JSON should be a simple map of string to integer: `{"filename": value, ...}`.

Please implement the Go program, run it, and generate the final `/home/user/results.json` file.