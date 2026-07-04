You are an engineer setting up the core of a polyglot build system. This system uses custom configuration files containing mathematical formulas to define build constants and performance-critical mathematical operations. Your task is to write a Python script that acts as our custom compiler and test runner.

There is a configuration file located at `/home/user/formulas.txt` containing the following lines:
```
ALPHA = 25 + 3 * (12 - 4)
BETA = ALPHA * 2 - 15
compute(x) = x * x * x - ALPHA * x + BETA
```

You must write a Python script at `/home/user/build_system.py` that does the following:
1. **Expression Parsing:** Parse `/home/user/formulas.txt`. Evaluate `ALPHA` and `BETA` dynamically (assume strictly integer arithmetic).
2. **Code Translation:** Generate two source files implementing the `compute(x)` numerical algorithm, replacing `ALPHA` and `BETA` with their statically evaluated integer values:
   - A C program at `/home/user/impl.c` that accepts a single integer `x` as a command-line argument, computes the result, and prints it to stdout.
   - A Python module at `/home/user/impl.py` containing a function `def compute(x):` that returns the computed integer.
3. **Compilation:** Use `gcc` to compile `/home/user/impl.c` into an executable at `/home/user/impl_bin`.
4. **Integration Testing:** Run a test loop for integer inputs `x` from `1` to `5` (inclusive). For each `x`, execute `/home/user/impl_bin x` and call `compute(x)` from `impl.py`.
5. **Reporting:** Verify that both implementations return identical results. Write the evaluated constants and the test arrays to a JSON file at `/home/user/validation.json` in the exact following format:
```json
{
  "ALPHA": <integer>,
  "BETA": <integer>,
  "c_results": [<res_1>, <res_2>, <res_3>, <res_4>, <res_5>],
  "py_results": [<res_1>, <res_2>, <res_3>, <res_4>, <res_5>],
  "match": <boolean>
}
```

Ensure all paths are absolute and the JSON format is strictly valid. Run your Python script to generate the final artifacts.