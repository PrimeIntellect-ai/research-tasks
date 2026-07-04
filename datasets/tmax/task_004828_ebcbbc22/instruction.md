You are a mobile build engineer maintaining a CI pipeline for a Python package that wraps a C library. The recent pipeline runs are failing because of a broken setup configuration and a bug in the C library.

You have been given a workspace at `/home/user/workspace` containing the following files:
- `mathops.c`: A Python C-extension implementing math operations.
- `setup.py`: A broken setup script for the C-extension.
- `fix.patch`: A patch file that fixes a logical bug in `mathops.c`.

Your task is to complete the following steps to get the pipeline green:
1. Apply the patch `/home/user/workspace/fix.patch` to `/home/user/workspace/mathops.c`.
2. Fix the `setup.py` script so that it correctly compiles `mathops.c` into the `mathops` module.
3. Write a property-based test in `/home/user/workspace/test_mathops.py` using the `pytest` and `hypothesis` libraries. 
   - You must import `mathops`.
   - Write a test function `test_add` that uses `@given(st.integers(), st.integers())` from `hypothesis.strategies` to verify that `mathops.add(a, b)` correctly returns the sum of `a` and `b`.
4. Create a CI script at `/home/user/workspace/ci_run.sh` that:
   - Compiles the C-extension in-place (`python3 setup.py build_ext --inplace`).
   - Runs the tests using `python3 -m pytest test_mathops.py`.
   - Exits with code 0 on success.

Ensure that `/home/user/workspace/ci_run.sh` is executable. You can use standard Linux utilities and python commands.