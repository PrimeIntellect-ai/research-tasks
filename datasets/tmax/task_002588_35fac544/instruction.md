You are an open-source maintainer reviewing a pull request for a project called "MathStack", a web-based mathematical expression evaluator that processes Reverse Polish Notation (RPN). 

A contributor has submitted a PR to replace the core evaluation logic with a C extension for performance, but the CI pipeline is failing. The code is located in `/home/user/math_pr/`.

The project consists of:
1. `server.py`: A simple HTTP server that routes requests like `/eval/<expression>` to the evaluator.
2. `mathstack.c`: The newly contributed C extension for the evaluator.
3. `setup.py`: The build script for the C extension.

There are three major issues you need to fix:
1. **URL Routing Bug**: In `server.py`, the routing logic extracts the expression from the URL path but fails to decode URL-encoded characters (like `%20` for spaces or `%2D` for minus signs). Fix it so that the extracted expression string is correctly unquoted before being passed to `mathstack.eval()`.
2. **C/C++ Memory Safety / Buffer Overflow**: `mathstack.c` has a fixed, critically small stack size (`int stack[5];`). If an expression requires a stack depth greater than 5, it causes a buffer overflow and segfaults. Modify `mathstack.c` to support a stack depth of up to 100 items safely.
3. **Code Translation Error**: The original Python evaluator used floor division (`//`) for the `DIV` operation. The C extension currently uses C's standard integer division (`/`), which truncates towards zero. This causes a mismatch when dividing negative numbers (e.g., `-17 DIV 5` should yield `-4`, but the C version yields `-3`). Update the `DIV` logic in `mathstack.c` to match Python's floor division behavior.

**Instructions**:
1. Fix the issues in `server.py` and `mathstack.c`.
2. Build and install the C extension locally using `python3 setup.py build_ext --inplace`.
3. Start the server on port 8080 (e.g., `python3 server.py &`).
4. Evaluate the following URL-encoded RPN expression by making an HTTP GET request to your local server:
   `/eval/-17%205%20DIV%202%20MUL%2010%2010%2010%2010%2010%2010%20ADD%20ADD%20ADD%20ADD%20ADD%20ADD`
   *(This decodes to: `-17 5 DIV 2 MUL 10 10 10 10 10 10 ADD ADD ADD ADD ADD ADD`)*
5. Save the plain-text numeric response of that specific `curl` request to `/home/user/verification.log`.

Do not change the names of the files or the core architecture. Just apply the necessary bug fixes.