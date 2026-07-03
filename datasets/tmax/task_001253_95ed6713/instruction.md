You are an engineer tasked with fixing a broken polyglot build system and completing a multi-language microservice.

In `/home/user/polymath/`, there are two subdirectories:
1. `node_api/` - A Node.js Express server that should expose a math evaluation REST API.
2. `python_client/` - A Python wrapper package that bundles and manages the Node.js server.

The project is currently broken in three ways:
1. **Broken Build System**: The Python package's `/home/user/polymath/python_client/setup.py` is incomplete. When someone runs `pip install .` inside `python_client`, it is supposed to automatically run `npm install` inside `../node_api` and copy the entire `node_api` folder (including `node_modules`) into the bundled Python package data (so it exists alongside `__init__.py` inside the site-packages `poly_calc` directory). You must fix `setup.py` to hook into the setuptools build process to achieve this.
2. **Missing API & Expression Parser**: The Node server `/home/user/polymath/node_api/server.js` is missing its core route. Implement a `POST /calc` REST endpoint that accepts a JSON payload `{"expression": "..."}`. The expression will contain positive integers, spaces, and the operators `+`, `-`, `*`, `/`, as well as parentheses `(` and `)`. You must implement a parser and evaluator that respects standard order of operations (PEMDAS). **You are strictly forbidden from using `eval()` or the `Function` constructor.** The endpoint must return `{"result": <number>}`.
3. **Missing Integration Test**: You need to write a script at `/home/user/test_run.py` that:
   - Imports the installed `poly_calc` package.
   - Starts the Node server using the package's internal start method.
   - Evaluates the expression `"14 + 2 * ( 18 - 6 ) / 4"` using the package's evaluate method.
   - Writes the exact JSON response from the server to `/home/user/polymath/results.log`.
   - Stops the server gracefully.

The `python_client/poly_calc/__init__.py` already contains a `PolyCalcClient` class with `start_server()`, `stop_server()`, and `evaluate(expr)` methods. It expects `server.js` to be in the `node_api` directory next to `__init__.py`.

Complete the build script, implement the Node.js parser/API, install the python package using `pip install .` from `python_client`, and finally execute `/home/user/test_run.py` to generate the log file.