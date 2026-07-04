You are tasked with building the backend for a new web-based mathematical evaluation tool. The system uses a highly optimized (but currently buggy) C library to evaluate Reverse Polish Notation (RPN) expressions, and a Python web service to expose this functionality. 

Here are your objectives:

1. **Fix the C Evaluator:**
   In `/home/user/evaluator.c`, there is a C function `int evaluate_rpn(const char* expr)` that computes the result of an RPN expression (supporting positive integers, `+`, and `*` separated by spaces). 
   Unfortunately, the current implementation has serious memory safety issues (buffer overflows and stack overflows) when handling large expressions. Refactor and fix `evaluator.c` to be completely memory safe and support expressions with up to 2000 tokens.
   
2. **Polyglot Build & Integration:**
   Write a build script (or use Python's `ctypes` / `cffi`) to compile `evaluator.c` into a shared library (`libevaluator.so`). Create a Python module that wraps this C function so it can be called safely from Python.

3. **Web Service implementation:**
   Create a Python HTTP web service (using Flask, FastAPI, or simple `http.server`) that listens on `0.0.0.0:8080`. 
   The service must implement the following REST endpoints:
   - `POST /evaluate`: Accepts a JSON payload `{"expression": "<rpn_string>"}`. Returns JSON `{"result": <integer_result>}`.
   - `GET /image`: There is an image located at `/app/equation.png` containing a handwritten or printed RPN expression. Use OCR (e.g., `pytesseract`) to extract the expression from this image, evaluate it using your C library, and return the result as JSON `{"result": <integer_result>}`.

4. **Service Startup:**
   Write a script `/home/user/start.sh` that compiles the C code, installs any needed Python dependencies, and starts the web service on port 8080. The service must remain running in the foreground or background so that it can be tested. Ensure the server does not require authentication.

Make sure your C code does not leak memory and handles edge cases gracefully (though you may assume all inputs from the test suite are valid RPN expressions). Start the server and leave it running.