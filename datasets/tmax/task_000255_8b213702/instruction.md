You are tasked with migrating a mathematical API service from Python 2 to Python 3. The legacy system relies on an Nginx reverse proxy, a Redis cache, and a backend Python service that uses a proprietary C-extension for mathematical calculations. Because the C-extension is incompatible with Python 3 and its source is lost, you must reverse-engineer its behavior from a provided binary oracle and reimplement it purely in Bash.

System State:
- `/app/nginx/nginx.conf`: Nginx configuration file. Nginx runs on port 8080.
- Redis runs locally on port 6379.
- `/app/backend/`: Contains the Python API code. 
- `/app/backend/pyproject.toml`: The package configuration, which is currently broken and specifies outdated, conflicting dependencies incompatible with Python 3.
- `/app/legacy_oracle`: A stripped standalone Linux binary of the mathematical function. It takes two arguments: a semantic version string (e.g., `1.2.3`) and an integer `N`.

Your tasks:
1. **Fix Package Configuration**: Update `/app/backend/pyproject.toml` so the backend can be built and installed in a Python 3 environment. Remove the failing legacy C-extension dependency (`legacy-math-ext`), update the `flask` and `redis` package requirements to modern versions, and ensure `pip install .` runs successfully.
2. **Reimplement the Math Oracle**: Create a Bash script at `/home/user/math_worker.sh`. It must take the exact same arguments as `/app/legacy_oracle` (a semantic version string and an integer) and output the exact same integer result. You must use Bash arithmetic and standard CLI tools to precisely mimic the binary's logic. (Hint: run `/app/legacy_oracle` with different inputs to reverse-engineer its behavior. It performs a specific algorithmic combination of the version components and the integer).
3. **Integrate**: Modify the Python 3 backend (`/app/backend/app.py`) to execute `/home/user/math_worker.sh` via `subprocess` instead of importing the missing C-extension.
4. **Service Configuration**: Update `/app/nginx/nginx.conf` to proxy requests from `http://localhost:8080/api/math` to the Python 3 Flask service running on `http://localhost:5000`. Start the Flask application on port 5000.

Verification:
- The automated verifier will fuzz `/home/user/math_worker.sh` against `/app/legacy_oracle` with random semantic versions and integers to ensure bit-exact output equivalence.
- The verifier will start Nginx and Redis, then send HTTP GET requests to `http://localhost:8080/api/math?v=<semver>&n=<int>` to ensure the entire multi-service compose flow works and returns the correct result calculated by your Bash script.