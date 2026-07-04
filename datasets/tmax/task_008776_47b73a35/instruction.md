You are an open-source maintainer reviewing a Pull Request for a polyglot expression evaluation engine called `expr-eval`, located at `/home/user/expr-eval`. The core engine is written in Rust for performance and exposes a Python module using `PyO3` and `maturin`.

The PR author attempted to refactor the tokenization logic in the Rust core and added property-based tests in Python to verify the evaluation of Reverse Polish Notation (RPN) mathematical expressions. However, the CI pipeline is failing.

Your tasks are:
1. Attempt to build the Python extension in `/home/user/expr-eval` by running `maturin develop`. You will notice it fails with a Rust borrow checker/ownership error.
2. Fix the compilation error in the Rust source code (`/home/user/expr-eval/src/lib.rs`). 
3. After successfully compiling, run the property-based tests suite using `pytest /home/user/expr-eval/tests/test_eval.py`.
4. The tests use `hypothesis` to check mathematical invariants. The tests will fail because the PR author also introduced logical bugs in the RPN expression evaluator (specifically in non-commutative operations).
5. Debug and fix the logical bugs in the Rust expression parser/evaluator.
6. Re-compile the extension and verify that all tests pass.
7. Once all tests pass, run `pytest /home/user/expr-eval/tests/test_eval.py > /home/user/test_results.txt` to save the successful test output.

Ensure that the final output file `/home/user/test_results.txt` contains the passing test results, and that `/home/user/expr-eval/src/lib.rs` contains the corrected Rust code.