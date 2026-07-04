You are a systems programmer working on a polyglot mathematical evaluation server. The system consists of a high-performance C library (`libmathparser`) that evaluates Reverse Polish Notation (RPN) expressions, and a C++ server (`server.cpp`) that exposes this functionality over a raw TCP text protocol (simulating a WebSocket-like stream).

Currently, the CI/CD pipeline is broken. You need to fix the repository located at `/home/user/project`.

Here are the issues:
1. **Linking Error**: The polyglot build fails. The C++ server cannot link against the C library due to an "undefined reference" error when calling `evaluate_rpn`. You must identify and fix the interoperability issue between C and C++.
2. **Mathematical Bug**: Once compiled, the integration tests fail because the math parser computes division incorrectly. For example, the RPN expression `10 2 /` should evaluate to `5.0`, but it currently returns `0.2`. You must fix the logical bug in the C library.
3. **Build Orchestration**: The `Makefile` has a target `ci` that is supposed to build the project, start the server in the background, run the Python integration tests (`tests/test_client.py`), and gracefully shut down the server.

Your tasks:
1. Fix the codebase so that it compiles successfully.
2. Fix the division bug in the RPN evaluator.
3. Run `make ci` successfully.
4. Redirect the standard output of a successful `make ci` run to exactly `/home/user/project/ci_success.log`.

The automated tests will verify that `/home/user/project/ci_success.log` exists, contains the passing test output, and that the underlying files have been correctly patched.