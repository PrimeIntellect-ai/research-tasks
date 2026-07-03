You are an engineer tasked with porting a legacy configuration tool to run in a minimal container. The minimal container does not have Python installed. The existing tool relies on a Python C-extension (`expr_ext.c`) to parse and evaluate mathematical expressions in configuration files.

Your task is to extract the core algorithmic logic out of the Python FFI boilerplate, make it a pure C shared library, and write a standalone C program to parse the configuration.

Here is the current state of the system in `/home/user/legacy_tool`:
- `expr_ext.c`: A Python module written in C containing a basic expression evaluation function (currently bound to the Python C-API).
- `config.txt`: A structured configuration file with key-expression pairs.

Do the following:
1. Create a directory `/home/user/port`.
2. Extract the underlying math evaluation logic from `/home/user/legacy_tool/expr_ext.c` and remove all Python-specific code (`#include <Python.h>`, `PyObject`, method definitions, etc.).
3. Save the pure C logic as `/home/user/port/libexpr.c` and create a corresponding header `/home/user/port/libexpr.h`. The header must expose exactly one function: `double evaluate(const char* expression);`.
4. Write a standalone C program `/home/user/port/config_parser.c`. This program must:
   - Accept an input file path and an output file path as command-line arguments.
   - Read the input file line-by-line. Each line contains a key and an expression separated by a colon and a space (e.g., `Key: NUM OP NUM`).
   - Use the `evaluate` function from `libexpr` to compute the result of the expression.
   - Write the parsed configuration to the output file in the format `Key=Value\n`, where `Value` is formatted to exactly two decimal places (e.g., `%.2f`).
5. Write a `/home/user/port/Makefile`. Running `make` in `/home/user/port` should:
   - Compile `libexpr.c` into a shared library named `libexpr.so`.
   - Compile `config_parser.c` and link it dynamically against `libexpr.so` to produce an executable named `config_parser`.
6. Run your compiled `config_parser`, passing `/home/user/legacy_tool/config.txt` as the input and `/home/user/port/output.txt` as the output.

Ensure that `/home/user/port/output.txt` is accurately generated. The verification process will check your Makefile, your C code's lack of Python dependencies, and the precise contents of `output.txt`.