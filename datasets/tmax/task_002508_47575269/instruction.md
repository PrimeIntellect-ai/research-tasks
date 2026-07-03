You are an engineer tasked with porting and integrating a hybrid Go/Python calculation tool. 

In `/home/user/workspace`, you will find a Go project in the `go_calc` directory and a file named `program.txt`.

The Go project is supposed to compile into a C-shared library (`libcalc.so`) that performs arithmetic operations utilizing goroutines and channels internally. However, the Go code currently fails to build due to a circular import between the `ops` and `util` packages.

Your task:
1. Fix the circular dependency in the Go code inside `/home/user/workspace/go_calc` without changing the mathematical logic or the signature of the exported `Compute` function.
2. Build the Go project as a shared library named `libcalc.so` in `/home/user/workspace`.
3. Write a Python script at `/home/user/workspace/evaluator.py` that parses and evaluates the custom stack-based language found in `/home/user/workspace/program.txt`.

The language in `program.txt` consists of instructions on separate lines:
- `PUSH <int>`: pushes an integer onto the stack.
- `ADD`: pops two integers, adds them, and pushes the result. (Operation code: 1)
- `SUB`: pops two integers, subtracts the first popped from the second popped (i.e., `top-1 - top`), and pushes the result. (Operation code: 2)
- `MUL`: pops two integers, multiplies them, and pushes the result. (Operation code: 3)
- `PRINT`: pops the top integer and appends it to the results log.

Your Python script must:
- Use a state machine/loop to parse the file line-by-line.
- Maintain a stack for the evaluations.
- Use `ctypes` to load `libcalc.so` and call the exported `Compute` function for all `ADD`, `SUB`, and `MUL` operations. The `Compute` function has the C signature: `int Compute(int a, int b, int op_code)`. Note that `a` is the left operand (e.g., `top-1`) and `b` is the right operand (e.g., `top`).
- Write the output of each `PRINT` instruction on a new line to `/home/user/workspace/results.txt`.

Everything must be automated. Write the Python script, compile the Go library, and execute the Python script so that `/home/user/workspace/results.txt` is populated correctly.