You are a platform engineer setting up a polyglot build and test system for a new mathematical library. We have a C++ program that performs numerical integration using Simpson's 1/3 rule, and a Python test suite to verify its correctness.

Currently, the C++ code has a bug in its numerical algorithm implementation (the Simpson's rule coefficients are swapped), and there is no build system tying the languages together. 

Your tasks are to:

1. Fix the numerical bug in `/home/user/polymath/src/integrate.cpp`. The function $f(x) = x^3$ is being integrated. In Simpson's 1/3 rule, the sum over interior points should multiply odd-indexed terms by 4 and even-indexed terms by 2. The current code does the reverse.
2. Create a unified patch file of your fix. Save the diff between the original buggy file and your fixed file as `/home/user/polymath/simpson.patch`.
3. Create a `Makefile` in `/home/user/polymath` from scratch. It must have the following targets:
   - `build`: Compiles `src/integrate.cpp` into a binary located at `bin/integrate` (create the `bin` directory if it doesn't exist). Use `g++` with standard flags.
   - `test`: Executes the Python test suite located at `tests/test_integration.py` using `pytest`. This target should depend on `build`.
   - `clean`: Removes the `bin` directory.
4. Run your build and test pipeline to ensure everything works. When you are done, `make test` should execute successfully, passing the end-to-end orchestration tests.

Assume `g++`, `python3`, and `pytest` are already available or can be installed via `apt-get` / `pip` if necessary. All work should be strictly contained within `/home/user/polymath`.