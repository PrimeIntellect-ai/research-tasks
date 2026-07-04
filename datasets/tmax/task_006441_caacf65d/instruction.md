You are an open-source maintainer reviewing a pull request for a Python package called `math-ws-proxy`. The contributor attempted to upgrade the package to use a new build system, implement a numerical constraint satisfaction solver over WebSockets, and add database migrations. However, the PR is broken.

Your task is to fix the repository located at `/home/user/math-ws-proxy` by completing the following steps:

1. **Fix the Build System (`pyproject.toml`)**
   The `pyproject.toml` is malformed and missing a required dependency. Fix it so that running `pip install .` inside `/home/user/math-ws-proxy` successfully installs the package and the `websockets` library (version `>=10.0`). The package name should be `math-ws-proxy` and the source code is located in the `src` directory.

2. **Fix the Constraint Satisfaction Solver (`src/math_ws/solver.py`)**
   The solver is supposed to find the smallest positive integer `x` (where `x >= 1`) and the corresponding positive integer `y` (where `y >= 1`) that satisfies the linear Diophantine equation:
   `a * x + b * y = c`
   Given strictly positive integers `a`, `b`, and `c`.
   Currently, the function `solve_diophantine(a, b, c)` in `src/math_ws/solver.py` is broken. Implement it so it returns a tuple `(x, y)` satisfying the constraints, or `None` if no such positive integers exist.

3. **Complete the Schema Migration (`migrate.py`)**
   The repository includes a script `/home/user/math-ws-proxy/migrate.py` and a legacy SQLite database `/home/user/math-ws-proxy/legacy.db`.
   The legacy DB has a table `requests` with schema `(id INTEGER PRIMARY KEY, equation TEXT)`. The `equation` column contains strings strictly in the format `"ax + by = c"` (e.g., `"3x + 4y = 25"`).
   Write Python code in `migrate.py` to:
   - Connect to `legacy.db`
   - Read all rows
   - Create a new database `/home/user/math-ws-proxy/v2.db` with a table `parsed_requests` having schema: `(id INTEGER PRIMARY KEY, a INTEGER, b INTEGER, c INTEGER)`
   - Parse the `equation` strings and insert the integer values of `a`, `b`, and `c` into `v2.db` with the corresponding `id`.

4. **Create a Reverse Proxy Configuration (`nginx.conf`)**
   The application runs a WebSocket server on port `9000`. We need to put it behind an Nginx reverse proxy.
   Create an Nginx configuration file at `/home/user/nginx.conf` that:
   - Runs in the foreground (or testable via `nginx -t`) - include `pid /tmp/nginx.pid;` and use a writable `error_log /tmp/error.log;`.
   - Has an `events {}` block.
   - Has an `http` block with `access_log /tmp/access.log;` and `client_body_temp_path /tmp/client_body;` `proxy_temp_path /tmp/proxy_temp;` `fastcgi_temp_path /tmp/fastcgi_temp;` `uwsgi_temp_path /tmp/uwsgi_temp;` `scgi_temp_path /tmp/scgi_temp;`.
   - Has a `server` block listening on port `8080`.
   - Proxies all requests (`location /`) to `http://127.0.0.1:9000`.
   - Includes the necessary headers to correctly upgrade the connection to a WebSocket (`Upgrade $http_upgrade` and `Connection "upgrade"`).

Verify your setup by ensuring `pip install .` works, the python tests for the solver pass, `python migrate.py` successfully generates `v2.db`, and `nginx -t -c /home/user/nginx.conf` reports a successful configuration test.