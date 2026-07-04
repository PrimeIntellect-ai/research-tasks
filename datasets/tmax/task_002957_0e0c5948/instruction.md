You are a developer tasked with debugging a failing Continuous Integration (CI) build for an internal mathematics library. 

The source code is located in `/home/user/optimization_lib`. 
Currently, running `pytest` in this directory results in test failures due to a `ConvergenceError` in our custom root-finding algorithm. The original author left recently, and it's suspected they introduced a typo in the numerical update step of the algorithm before leaving.

Your tasks are to:
1. Run the existing tests, analyze the traceback, and understand the existing codebase in `/home/user/optimization_lib/solver.py`.
2. Identify and fix the mathematical/logical bug causing the algorithm to diverge or fail to converge. 
3. Create a new regression test file at `/home/user/optimization_lib/tests/test_regression.py`.
4. Inside `test_regression.py`, write a test function named `test_regression_quadratic()`. This test should use the fixed `newton_root_finder` to find the root of the function $f(x) = x^2 - 9$ with its derivative $df(x) = 2x$. Start the search at $x_0 = 5.0$. 
5. The regression test must assert that the returned root is within `1e-4` of `3.0`, and that the number of iterations taken was strictly less than `10`.

Make sure that after your changes, running `pytest /home/user/optimization_lib` completes with 100% passing tests (both the original tests and your new regression test).