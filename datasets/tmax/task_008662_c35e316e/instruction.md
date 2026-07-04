You are an engineer tasked with creating a polyglot build system and embedded expression evaluator from scratch. Your goal is to write a Python script that parses a custom domain-specific language (DSL), compiles C source code into a shared library, dynamically loads the compiled library to resolve C ABI functions, and interprets a nested expression using those loaded functions.

We have an initial directory located at `/home/user/polybuild`. 
Inside this directory, there are two files:

1. `math_ops.c`: Contains a set of simple mathematical operations exported as C functions.
2. `poly.dsl`: A configuration file written in our custom DSL.

The custom DSL in `poly.dsl` contains exactly two lines with the following syntax:
Line 1: `BUILD shared <lib_alias> <c_source_file>`
Line 2: `EVAL <lib_alias> <s_expression>`

Your task is to create a Python script at `/home/user/polybuild/polybuild.py` that does the following:
1. Opens and reads `/home/user/polybuild/poly.dsl`.
2. Parses the `BUILD` command. It must invoke the system's GCC compiler (using `subprocess`) to compile the specified `<c_source_file>` into a shared library named `lib<lib_alias>.so` in the same directory. The C code should be compiled with `-fPIC` and `-shared`.
3. Parses the `EVAL` command. This involves:
   a. Loading the newly compiled shared library `lib<lib_alias>.so` using Python's `ctypes` module.
   b. Parsing the `<s_expression>`, which is a Lisp-like nested expression (e.g., `(op_add (op_mul 5 6) 2)`). 
4. Implements an interpreter that evaluates the parsed S-expression. 
   - If a node in the expression is an integer, it evaluates to that integer.
   - If a node is a function call (e.g., `op_add`), it dynamically resolves the corresponding function symbol from the loaded shared library via `ctypes`. Note: All functions in `math_ops.c` take two 32-bit signed integers (`int32_t`) as arguments and return a 32-bit signed integer. Your Python ctypes interface must be explicitly configured with `argtypes` and `restype` as `ctypes.c_int32` to correctly manage the ABI.
   - Recursively evaluate the arguments and pass them to the resolved C function.
5. Writes the final evaluated integer result of the `EVAL` expression to `/home/user/polybuild/result.out` as a plain text string (e.g., "42").

You must run your Python script once it is complete to ensure `libop_lib.so` is compiled and `result.out` is generated.