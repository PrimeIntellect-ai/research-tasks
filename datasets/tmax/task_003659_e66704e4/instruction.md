I have an old Python 2 data processing service that evaluates complex mathematical expressions and delegates heavy numerical computations to a high-performance backend. I need you to migrate the main service to Python 3 and fix a broken C/Rust backend extension so that the system works again.

Here is the current state of the system:
1. In `/home/user/legacy_math_api/`, there is a Python 2 script `app.py` that exposes a REST API using Flask. It parses mathematical expressions (like "2 * (sin(x) + 4)") and evaluates them.
2. The service relies on a compiled backend binary for the `evaluate_core` function. We only have a stripped binary of the old v1 backend at `/app/bin/core_evaluator_v1.bin`.
3. The previous developer started rewriting the core backend in Rust (located in `/home/user/rust_backend/`) with a C wrapper and Makefile in `/home/user/c_wrapper/`. However, the Makefile has a linking error, and the Rust code has a strict ownership/borrow checker issue in `src/lib.rs` involving mutable borrows during numerical array processing.
4. The REST API must run on `127.0.0.1:8080`.

Your tasks are:
1. **Migrate and Update the API:** Rewrite `/home/user/legacy_math_api/app.py` to be fully Python 3.10+ compatible. It must expose a `POST /evaluate` endpoint. The request body will be JSON: `{"expression": "...", "x_value": 3.14}`. It should return JSON: `{"result": <float>}`.
2. **Reverse Engineer the Binary:** Analyze the stripped binary at `/app/bin/core_evaluator_v1.bin` to understand the numerical algorithm it applies to the parsed expression coefficients. 
3. **Fix the Backend Build:** Fix the borrow checker error in `/home/user/rust_backend/src/lib.rs` and the linking error in `/home/user/c_wrapper/Makefile` so that a shared library `libmathcore.so` is successfully built.
4. **Integrate:** Ensure the updated Python 3 REST API loads the new `libmathcore.so` using `ctypes` and correctly evaluates the expressions by calling the C/Rust backend. Start the Flask server in the background on `127.0.0.1:8080`. Create a log file at `/home/user/server.log` capturing the startup output. 

Please ensure the service is running on `127.0.0.1:8080` and is ready to accept HTTP POST requests on the `/evaluate` endpoint. Authentication is not required, but the API must strictly handle invalid mathematical expressions by returning a 400 status code with `{"error": "Invalid expression"}`.