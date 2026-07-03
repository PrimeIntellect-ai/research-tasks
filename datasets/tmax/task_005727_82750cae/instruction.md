You are a developer taking over a partially finished web security backend project. The project is an expression evaluator service written in Go, which offloads the parsing and evaluation of Reverse Polish Notation (RPN) math expressions to a high-performance C backend. 

Currently, the project files are disorganized, the CI/CD build script is misconfigured, and the C code contains a critical memory safety vulnerability.

Your task is to fix the project in `/home/user/expr_project`.

1. **Organize and Fix the Build:**
   The build script `/home/user/expr_project/build.sh` is failing. It is currently disabling CGO and failing to build the project. Reorganize the project files so that `main.go`, `eval.c`, and `eval.h` are correctly associated for `cgo` to compile them together. Update `build.sh` to compile the application into an executable named `expr_app` in the `/home/user/expr_project` directory.

2. **Fix Memory Safety (Undefined Behavior):**
   The C backend (`eval.c`) implements a stack for evaluating RPN expressions. However, the stack has a fixed size of 4 (`int stack[4];`), and the code currently has no bounds checking, leading to buffer overflows when evaluating complex expressions. Modify `eval_rpn` in `eval.c` so that if a push operation exceeds the stack bounds (i.e., trying to push when `sp >= 4`), the function immediately returns `-999`.

3. **Evaluate and Log:**
   Once fixed and compiled, run the compiled `./expr_app` with the following RPN expression:
   `"10 5 2 * + 8 4 / - 3 +"`
   
   The application will print the result. Save this exact numeric result to `/home/user/result.log`.

**Constraints:**
- Do not change the overall logic of the RPN evaluator, only add the memory safety bounds check.
- The Go program and C code must successfully compile using the `./build.sh` script.