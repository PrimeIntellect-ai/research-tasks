I need you to help me migrate a legacy Python 2 web application to Python 3. The application is a simple mathematical expression evaluator API, but it is currently highly insecure because it uses Python's built-in `eval()` function, and its dependencies are completely outdated. 

Here is what you need to do:

1. **Setup and Package Management:**
   - I have placed the legacy Python 2 project in `/home/user/legacy_project`. It contains an `app.py` and a `requirements.txt`.
   - Create a new directory `/home/user/modern_project`.
   - Create a Python 3 virtual environment in `/home/user/modern_project/venv`.
   - Create an updated `requirements.txt` in `/home/user/modern_project` that specifies `Flask>=2.0.0` and `Werkzeug>=2.0.0`. Install these dependencies in your new virtual environment.

2. **Code Migration & Routing (Python 3):**
   - Port the legacy `app.py` to `/home/user/modern_project/app.py` using Python 3. 
   - The application must be a Flask app with a single GET endpoint: `/evaluate`.
   - The endpoint must accept a query string where `expr` contains a mathematical expression (e.g., `expr=x*y+z`).
   - Any other query parameters provided should be treated as variable assignments (e.g., `x=2&y=3&z=4`). All variable values will be integers.

3. **Safe Expression Evaluation (AST):**
   - Remove the dangerous `eval()` call.
   - Implement a safe expression evaluator using Python's built-in `ast` module (`ast.parse`).
   - The evaluator must support integer arithmetic with the following operators: Addition (`+`), Subtraction (`-`), Multiplication (`*`), and Division (`/` - standard float division).
   - It must support variable substitution using the parsed query parameters.
   - Return the result as a plain text string. If a variable is missing or the expression is invalid, return the string `ERROR` with a 400 status code.

4. **Verification:**
   - Write a python script at `/home/user/test_app.py` that uses the Flask test client (from `/home/user/modern_project/app.py`) to test the following URLs and writes the raw text response body of each to `/home/user/results.log`, each on a new line:
     1. `/evaluate?expr=a*b%2B2&a=5&b=3` (Note: `%2B` is URL-encoded `+`)
     2. `/evaluate?expr=x/y-z&x=10&y=2&z=1`
     3. `/evaluate?expr=foo*bar&foo=7` (This should fail due to missing `bar`)

Execute the necessary commands to install the dependencies, write the migrated code, and run your `test_app.py` script so that `/home/user/results.log` is generated.