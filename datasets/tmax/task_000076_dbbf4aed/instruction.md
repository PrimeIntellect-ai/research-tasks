You are a platform engineer optimizing a CI/CD pipeline. One of the pipeline stages runs a dependency constraint solver to find compatible package versions. Currently, the validation step is entirely written in Python and is too slow to evaluate the large search space. 

Your goal is to translate the core constraint checking logic into C, compile it into a shared library, and use Python's `ctypes` (Foreign Function Interface) to create a much faster hybrid solver.

The slow reference implementation is located at `/home/user/pipeline/reference.py`:

```python
# /home/user/pipeline/reference.py

def evaluate_constraints(v1: int, v2: int, v3: int, v4: int) -> int:
    """
    Returns 1 if the package version combination satisfies all mathematical constraints, 0 otherwise.
    """
    c1 = (3 * v1 + 5 * v2 + v3 - 2 * v4) == 99
    c2 = (v1 * v1 + v2 * v3 - v4) == 283
    c3 = (v1 + v2 + v3 + v4) == 48
    
    if c1 and c2 and c3:
        return 1
    return 0
```

Your tasks are:
1. Create a C file at `/home/user/pipeline/evaluate.c` that implements the exact same logic in a C function named `evaluate_constraints`. It must take four `int` parameters and return an `int`.
2. Compile this C file into a shared library named `/home/user/pipeline/libevaluate.so`.
3. Create a Python script at `/home/user/pipeline/solver.py` that uses the `ctypes` module to load `/home/user/pipeline/libevaluate.so` and call the C function.
4. Using your new hybrid Python/C solver, write a loop in `solver.py` to search the space of all possible version combinations where `v1`, `v2`, `v3`, and `v4` each range from `1` to `50` (inclusive).
5. Find the single combination of `(v1, v2, v3, v4)` that satisfies the constraints.
6. Write the resulting combination to a file located at `/home/user/pipeline/solution.txt` in the exact format: `v1,v2,v3,v4` (e.g., `10,20,30,40`).

Ensure all files are created in the `/home/user/pipeline` directory. You may run the scripts in your terminal to generate the final output.