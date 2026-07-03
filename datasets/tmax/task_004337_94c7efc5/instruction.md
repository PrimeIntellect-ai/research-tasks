Hello! I need help migrating our legacy mathematical evaluation engine from Python 2 to Python 3. The project currently fails to build and run due to a mix of outdated dependencies, Python 3 incompatibilities, and a buggy C extension that evaluates core mathematical expressions.

Here is what you need to do:

1. **Extract the Expression Grammar:**
   There is an image file located at `/app/grammar.png`. It contains the updated mathematical grammar rules (using standard EBNF-like syntax) that our parser must support. Use OCR (tesseract is available) to read the text from this image and save the extracted raw text to `/home/user/extracted_grammar.txt`.

2. **Migrate and Fix the Core Engine:**
   In `/home/user/math_engine`, you will find a Python 2 project.
   - Migrate `parser.py` and `server.py` to Python 3. 
   - The engine relies on a C extension located in `/home/user/math_engine/c_src/fast_eval.c`. This extension is supposed to parse and evaluate the expressions fast, but it currently has memory safety issues (buffer overflows and use-after-free bugs) that cause segmentation faults on large expressions.
   - Fix the C code, ensuring memory safety. Compile it so it can be imported by the Python 3 code.
   - Ensure the updated Python code correctly utilizes the C extension to evaluate expressions defined by the grammar you extracted.

3. **Benchmarking and Testing:**
   Write a benchmarking script at `/home/user/math_engine/benchmark.py` that evaluates 10,000 random expressions and asserts that the evaluation completes without crashing. Also, write unit tests in `/home/user/math_engine/test_eval.py` covering edge cases like division by zero and deeply nested parentheses.

4. **Reverse Proxy Configuration:**
   Our API runs locally on port 8080 (via `server.py`). Configure and start an Nginx reverse proxy that listens on port 80. It should route all traffic from `http://localhost/api/eval` to `http://127.0.0.1:8080/eval`. Ensure the Nginx service is running.

5. **Final CLI Wrapper for Verification:**
   Create an executable bash script at `/home/user/run_eval.sh` that takes a single mathematical expression as a string argument and prints the evaluated numeric result to stdout (using your migrated Python 3 engine). 
   *Example:* `./run_eval.sh "3 + 5 * (2 - 8)"` -> `-27`

Our automated systems will verify your setup by heavily fuzzing your `./run_eval.sh` script with random mathematical expressions and comparing the outputs bit-for-bit against a reference oracle.