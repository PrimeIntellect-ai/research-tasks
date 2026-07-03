You are a script developer building a fast C++ utility for evaluating a static dataflow circuit.

Your team lost the original configuration file for the production circuit, but managed to find a screenshot of the textual rules representing the dependency graph. This screenshot is located at `/app/circuit_def.png`.

Additionally, the current C++ codebase for the evaluator (located in `/home/user/src/`) was poorly written by a departed intern. It attempts to build an Abstract Syntax Tree (AST) to evaluate expressions, but it fails to compile or run correctly:
1. It contains severe memory management bugs (dangling pointers and memory leaks) that cause segmentation faults during graph traversal and evaluation.
2. It currently constructs a placeholder dummy circuit instead of the real one.

Your tasks are:
1. **Analyze the Image**: Extract the circuit's logic and graph structure from `/app/circuit_def.png`. The image describes how to compute the output from three inputs: `X`, `Y`, and `Z`.
2. **Debug and Fix Memory Issues**: Fix the C++ code in `/home/user/src/` so that it correctly and safely manages memory during AST construction and expression evaluation without any memory leaks or segfaults (you may use `valgrind` or `gdb`).
3. **Implement the True Circuit**: Update the C++ code to construct the specific AST graph described in the image.
4. **Build the Executable**: Compile your fixed C++ program. The final compiled executable must be located at `/home/user/evaluator`.

**Executable Specification:**
* Path: `/home/user/evaluator`
* Invocation: `./evaluator <X> <Y> <Z>` (where X, Y, and Z are integers).
* Output: A single integer printed to standard output representing the evaluated result of the circuit. No other text should be printed to standard output.

Ensure your compiled program produces the exact correct output for any combination of integer inputs.