You have inherited an unfamiliar codebase for a mathematical calculation service. The service is supposed to calculate the real root of a cubic polynomial $f(x) = ax^3 + bx^2 + cx + d$ using Newton's method. It exposes an HTTP API to serve requests.

However, the previous developer left it in a broken state:
1. **Dependency/Build Issues**: The `CMakeLists.txt` is misconfigured and conflicts with the system's libraries. You will need to resolve this to build the project.
2. **Convergence & Precision Bugs**: For certain coefficients, the HTTP request hangs indefinitely. The iterative solver has a loop termination bug and floating-point precision issues that prevent it from converging to the required tolerance (`epsilon = 1e-7`). 
3. **Black-box Oracle**: You are provided with a legacy stripped binary at `/app/oracle_solver`. You can execute it via `/app/oracle_solver a b c d` to get the correct real root. Use it to understand the expected behavior and verify your fixes.

Your objective is to:
1. Fix the build configuration so the project compiles successfully.
2. Debug and patch the C++ implementation in `/workspace/math_server/solver.cpp` to fix the infinite loops, convergence failures, and precision issues.
3. Build and run the HTTP service on `127.0.0.1:8080`.

The service must implement the following HTTP API:
- **Endpoint**: `POST /solve`
- **Request Body**: JSON `{"a": <float>, "b": <float>, "c": <float>, "d": <float>}`
- **Response**: JSON `{"root": <float>}` (accurate to at least 5 decimal places compared to the oracle).

The source code is located in `/workspace/math_server/`.
Keep the server running in the background on port 8080 once you have fixed the issues, so our automated verifier can test it.