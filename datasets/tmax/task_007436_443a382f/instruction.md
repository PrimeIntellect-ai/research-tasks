You are a backend utility developer modernizing a legacy mathematical expression evaluator. The existing system uses a poorly structured SQLite database to store math formulas and lacks an API.

Your task spans multiple phases: resolving dependencies, migrating the database schema, building a REST API, and writing test fixtures.

Working directory: `/home/user/math_api`

**Phase 1: Dependency Setup**
Initialize a Python environment and create a `requirements.txt` containing the necessary libraries to build a Flask (or FastAPI) REST API, interact with SQLite, evaluate mathematical expressions reliably using `sympy`, and test with `pytest`. 

**Phase 2: Schema Migration**
In `/home/user/math_api`, you will find an existing SQLite database named `legacy.db`. It contains a single table:
`old_formulas (id INTEGER PRIMARY KEY, title TEXT, math_string TEXT)`

Write a Python migration script named `migrate.py` that:
1. Connects to `legacy.db`.
2. Creates a new table named `expressions` with the schema: `(id INTEGER PRIMARY KEY, name TEXT, expression TEXT, version INTEGER DEFAULT 1)`.
3. Migrates all data from `old_formulas` to `expressions`, mapping `title` to `name` and `math_string` to `expression`.
4. Drops the `old_formulas` table.
Run this script to perform the migration.

**Phase 3: REST API Construction**
Create a web server in `/home/user/math_api/app.py` using your chosen web framework. It must connect to `legacy.db` and expose a single endpoint:
`POST /evaluate`

Request JSON payload:
```json
{
  "name": "formula_name",
  "variables": {
    "x": 2.5,
    "y": 4.0
  }
}
```

Behavior:
1. Lookup the `expression` in the `expressions` table by `name`.
2. Parse and evaluate the expression using the provided variables. Use `sympy` to handle the mathematical parsing and evaluation safely.
3. Return the result as a JSON response: `{"result": <evaluated_float_value>}`.
4. Run the server on port 5000 (ensure it listens on `127.0.0.1`).

**Phase 4: Test Fixtures and Mocks**
Create a test file `/home/user/math_api/test_app.py`. Use `pytest`.
1. Create a pytest fixture that sets up a temporary in-memory SQLite database (with the new `expressions` schema) and inserts a test record: `name="pythagoras"`, `expression="sqrt(a**2 + b**2)"`.
2. Mock or override the database connection in your API so the test uses this in-memory database instead of `legacy.db`.
3. Write a test function that makes a test client request to `POST /evaluate` with `name: "pythagoras"` and variables `{"a": 3, "b": 4}`, asserting that the response `result` is `5.0`.

You should test your code by starting the server and making curl requests, as well as running your pytest suite.