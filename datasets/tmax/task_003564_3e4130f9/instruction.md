We have a multi-file Rust project located in `/app/calculator` that currently fails to compile because a crucial numerical constant is missing from its source code. The exact value of this constant was saved in an image file at `/app/blueprint.png` by the original developer.

Your tasks are:
1. Extract the missing constant from `/app/blueprint.png`. You can use `tesseract` which is pre-installed in the environment.
2. Fix the Rust project by inserting the correct constant where it is missing, and compile it in release mode. The binary should take a single integer argument, perform its numerical algorithm using the constant, and print the integer result to standard output.
3. Write and run a Python HTTP server listening on `0.0.0.0:8888`. 
4. The Python server must expose a `POST` endpoint at `/calculate`. It should accept a JSON payload in the format `{"number": <integer>}`.
5. When the `/calculate` endpoint is hit, the Python server should orchestrate an end-to-end test run by invoking the compiled Rust binary with the provided number, capture the output, and return it as a JSON response in the format `{"result": <integer>}`.

Ensure your Python server is running and listening on port 8888 before you finish the task. You can use standard libraries like `http.server`, or install `flask`/`fastapi` if you prefer. Do not constrain the host to localhost; bind to `0.0.0.0`.