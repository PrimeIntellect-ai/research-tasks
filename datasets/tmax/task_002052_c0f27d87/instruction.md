You are a QA engineer tasked with setting up an end-to-end test suite for a newly developed gRPC service that evaluates postfix mathematical expressions. 

We have a directory at `/home/user/math_service` containing the initial prototype. Unfortunately, the developer left before finishing it, and there are several issues:
1. The protobuf definitions haven't been compiled to Python yet.
2. The server implementation in `/home/user/math_service/server.py` has some bugs in its numerical algorithm for evaluating postfix expressions (e.g., it might calculate subtraction or division backwards, and it entirely lacks support for the factorial `!` operator).
3. We don't have an automated way to test it against our dataset.

Your tasks are:
1. **Prepare the environment:** Install any necessary gRPC tools and compile the protobuf file `/home/user/math_service/math_service.proto` so it can be used by Python.
2. **Fix the Server:** Fix the bugs in `/home/user/math_service/server.py`. The service should support addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), exponentiation (`^`), and factorial (`!`). All numbers should be treated as floating-point. The factorial operator `!` is unary and should only apply to the single preceding value (e.g., `5 !` -> `120.0`). For binary operations, the order matters (e.g., `4 2 -` means `4 - 2`). If an invalid expression is sent, the server should return an error string in the response instead of crashing.
3. **Write the E2E Test Orchestrator:** Create a script at `/home/user/math_service/e2e_test.py`. This script should:
   - Read the structured test data from `/home/user/test_data.json`.
   - Start the gRPC server defined in `server.py` (or assume it's running in the background if you prefer to start it via shell, but orchestrating it inside the script or via bash wrapper is fine).
   - Send each expression to the gRPC service.
   - Parse the responses.
   - Write the results to `/home/user/test_results.json`.

The `/home/user/test_results.json` file must be a JSON array of objects, where each object corresponds to an entry in `test_data.json` and has the following exact keys:
- `"expression"`: The original string expression.
- `"expected"`: The expected result (float) or `null` if an error was expected.
- `"actual"`: The actual result (float) returned by the service, or `null` if the service returned an error message.
- `"status"`: `"PASS"` if `actual` equals `expected` (or if both are `null`), otherwise `"FAIL"`.

Example of a valid `test_results.json` entry:
```json
[
  {
    "expression": "3 4 + 2 *",
    "expected": 14.0,
    "actual": 14.0,
    "status": "PASS"
  }
]
```

Ensure all dependencies are installed, the server correctly evaluates all expressions, and the final `test_results.json` shows all tests passing.