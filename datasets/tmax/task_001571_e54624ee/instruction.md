You are a web developer optimizing a backend service. Your team has identified that a specific mathematical expression evaluation (Reverse Polish Notation) is a bottleneck in your Python application. To speed it up, a team member wrote a fast concurrent RPN interpreter in Go, but they left before integrating it.

Your task is to compile the Go interpreter into a shared library and write a Python integration script to use it.

1. You will find a Go source file at `/home/user/math_eval.go`. It contains an exported function `EvaluateRPN` that takes a C-string and returns a C-double.
2. Compile this Go code into a C-shared library named `/home/user/libmatheval.so`.
3. Write a Python script at `/home/user/test_integration.py`. This script must:
    - Use the `ctypes` module to load `/home/user/libmatheval.so`.
    - Correctly configure the argument types (string) and return type (double) for the `EvaluateRPN` function to handle the ABI properly.
    - Call the function with the following RPN expression: `"100 5 / 4 2 * + 2 /"`
    - Write the resulting float value (converted to a string) to `/home/user/math_output.txt`.

Ensure your Python script runs without errors and produces the correct output file.