You are tasked with setting up a build system and fixing a memory safety issue in a data processing pipeline. The pipeline involves generating mathematical expressions using a Python script, parsing and evaluating them in C++, and writing the results. 

The project is located at `/home/user/polyglot-eval`.

Currently, the C++ codebase has a severe memory safety issue (Undefined Behavior) that causes it to crash with a double-free or segmentation fault when processing certain expressions. Furthermore, there is no build system in place.

Here is what you need to do:

1. **Fix the C++ Undefined Behavior**: 
   The source code in `/home/user/polyglot-eval/src/` contains an AST-based expression parser and evaluator (`ast.h`, `ast.cpp`, `evaluator.cpp`, `main.cpp`). The `ASTNode` class manages memory manually but violates the Rule of Three, leading to a double-free when nodes are passed by value in `evaluator.cpp`. Refactor the memory management in `ast.h`/`ast.cpp` (e.g., using `std::unique_ptr` or properly implementing the copy constructor/assignment operator) to ensure memory safety and no leaks.

2. **Set up the Build System**:
   Create a `/home/user/polyglot-eval/CMakeLists.txt` from scratch that:
   - Sets the C++ standard to C++17.
   - Creates a library target `expr_lib` from `ast.cpp` and `evaluator.cpp`.
   - Creates an executable target `expr_eval` from `main.cpp` and links it against `expr_lib`.
   - Creates an executable target `test_runner` from `tests/test_runner.cpp` and links it against `expr_lib`.

3. **Create Test Fixtures**:
   Write a C++ test program at `/home/user/polyglot-eval/tests/test_runner.cpp`. It must include `ast.h` and `evaluator.h`. Create a simple test fixture that manually constructs an AST for `(10 + 20) * 2` and asserts that the evaluator returns `60`. The program should return `0` on success and non-zero on failure.

4. **Create the Pipeline Script**:
   Write a bash script at `/home/user/polyglot-eval/build_and_run.sh` that does the following:
   - Configures and builds the CMake project in `/home/user/polyglot-eval/build`.
   - Runs the `test_runner` executable.
   - If tests pass, invokes the provided Python script `/home/user/polyglot-eval/scripts/generate_data.py` (which outputs 1000 mathematical expressions to stdout).
   - Pipes the output of the Python script directly into the compiled `expr_eval` executable.
   - Redirects the standard output of `expr_eval` into `/home/user/polyglot-eval/results.txt`.

Ensure your `build_and_run.sh` has executable permissions and exits successfully only if all steps succeed.