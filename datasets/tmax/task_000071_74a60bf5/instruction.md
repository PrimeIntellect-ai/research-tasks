We are building a distributed, polyglot math evaluation API. I need you to set up the build orchestration, service configuration, and implement a strict security sanitizer for the mathematical expressions.

The workspace is located at `/app/`.

Here are your tasks:

1. **Polyglot Build Orchestration**
   Write a Python script at `/app/build_system.py` that compiles the backend services. 
   - Compile the C++ source `/app/src/cpp/engine.cpp` into the executable `/app/bin/engine_cpp`. (Requires `g++`).
   - Compile the Go source `/app/src/go/engine.go` into the executable `/app/bin/engine_go`. (Requires `go build`).
   Ensure the script creates the `/app/bin/` directory if it doesn't exist, and exits with code 0 on success.

2. **Expression Sanitizer (Adversarial Defense)**
   We are evaluating mathematical expressions, which is inherently risky in Python. Write a module `/app/src/python/sanitizer.py` containing a function `def is_safe_math(expression: str) -> bool:`.
   - The function must return `True` for safe math expressions and `False` for unsafe ones.
   - Safe expressions may contain digits, standard math operators (`+`, `-`, `*`, `/`, `**`, `^`, `()`, `.`), spaces, and the variables/constants `x`, `y`, `pi`, `e`.
   - Any attempt at code injection (e.g., `__import__`, `eval`, `os.system`), excessively long strings, or dangerous python constructs must be rejected.
   - The verifier will test your function against two corpora located at `/app/corpora/clean.txt` and `/app/corpora/evil.txt` (one expression per line). Your function must return `True` for 100% of the clean corpus and `False` for 100% of the evil corpus.

3. **URL Routing and Constraint Satisfaction**
   Complete the Flask application at `/app/src/python/app.py`. It provides a single endpoint `GET /evaluate?expr=...`.
   - First, run the `expr` through `is_safe_math()`. If it returns `False`, return HTTP 403.
   - If the expression contains the variable `x` or `y`, proxy the request to the C++ backend at `http://127.0.0.1:8082/eval?expr=...`.
   - If the expression contains `pi` or `e` (but not `x` or `y`), proxy it to the Go backend at `http://127.0.0.1:8081/eval?expr=...`.
   - Otherwise, evaluate it locally in Python (safely) and return the result as a string.

4. **Multi-Service Composition**
   Configure Nginx by writing a config file at `/app/nginx/nginx.conf`.
   - It should listen on port `8080`.
   - Route all requests starting with `/api/math/` to the Python Flask service at `http://127.0.0.1:8000/evaluate` (stripping the `/api/math/` prefix so that `/api/math/?expr=1+1` hits `/evaluate?expr=1+1` on the Flask app).

When you are finished, ensure that your build script has been run, the executables exist, and the services can be started together. (We will use our own runner to start the compiled binaries, the Flask app, and Nginx during verification).