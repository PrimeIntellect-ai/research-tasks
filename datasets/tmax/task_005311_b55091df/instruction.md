You are an engineer tasked with fixing and completing a polyglot math evaluation system. The system consists of a C shared library that evaluates Flattened Abstract Syntax Trees (ASTs) of mathematical expressions, and a Python wrapper that parses JSON formulas, migrates them into a custom C-compatible data structure, and invokes the C library.

Currently, the build system is broken, the C implementation is incomplete, and the Python migration/execution script is missing. 

Your tasks are:

1. **Fix the Build System**:
   There is a `Makefile` at `/home/user/math_system/Makefile` intended to build a shared library `libeval.so` from `eval.c`. It currently produces linking and compilation errors. Fix the `Makefile` so that running `make` correctly generates `libeval.so`. The library must be compiled as a shared library and link the math library.

2. **Complete the Numerical Evaluation (C)**:
   In `/home/user/math_system/eval.c`, the `evaluate_ast` function recursively evaluates a mathematical AST. However, the operations for Division (`OP_DIV` = 4) and Power (`OP_POW` = 5) are missing. 
   - Implement `OP_DIV`. If the denominator is `0.0`, return `0.0`.
   - Implement `OP_POW` (using `pow` from `<math.h>`).

3. **Schema Migration & Execution (Python)**:
   There is a legacy JSON file at `/home/user/math_system/formulas.json` containing a list of expressions. 
   Write a Python script at `/home/user/math_system/run.py` that:
   - Reads `formulas.json`.
   - Migrates each hierarchical JSON expression into a custom flattened array data structure. The C library expects a contiguous array of `Node` structs representing the AST:
     ```c
     typedef struct {
         int op;          // 0=VAL, 1=ADD, 2=SUB, 3=MUL, 4=DIV, 5=POW
         double value;    // Valid only if op == 0
         int left_idx;    // Index of the left child in the array (-1 if none)
         int right_idx;   // Index of the right child in the array (-1 if none)
     } Node;
     ```
     *Note: The root of the expression for each formula must be at index 0 in its array.*
   - Uses `ctypes` to load `libeval.so` and pass the flattened array to `double evaluate_ast(Node* nodes, int root_idx)`.
   - Evaluates all formulas and saves the results as a JSON object mapping the string `id` of the formula to its evaluated float result.
   - Saves the final JSON to `/home/user/math_system/results.json`.

**Example of `formulas.json` format**:
```json
[
  {
    "id": "f1",
    "expr": {"op": "add", "left": {"op": "val", "value": 5.0}, "right": {"op": "val", "value": 3.0}}
  }
]
```

To complete the task, ensure that `/home/user/math_system/results.json` exists and contains the correct evaluations.