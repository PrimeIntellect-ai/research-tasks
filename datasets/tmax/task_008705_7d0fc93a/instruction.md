I am migrating a legacy web backend from Python 2 to Python 3, and I need your help to fix the build system, update the code, and write a secure Bash CGI gateway to protect the application. 

Here is the situation:
The application lives in `/home/user/app/`. 
1. **Dependency Management**: The Python application relies on the `pyyaml` package. Create a Python 3 virtual environment at `/home/user/venv` and install `pyyaml` inside it.
2. **C Program Compilation & Makefile Repair**: The application uses a compiled C helper binary. The source file `helper.c` and its `Makefile` are in `/home/user/app/`. The `Makefile` is broken (it has spaces instead of tabs and is missing the math library flag `-lm` needed by `helper.c`). Fix the `Makefile`, compile the C code, and ensure the executable `helper_bin` is successfully built in `/home/user/app/`.
3. **Python Migration**: The script `/home/user/app/process.py` is written in Python 2. It has syntax errors in Python 3 (e.g., `print` statements) and uses the deprecated `yaml.load()` which needs to be updated to `yaml.safe_load()`. Update the script to be fully compatible with Python 3. It must execute successfully using the virtual environment's Python.
4. **Bash Gateway**: Write a secure CGI gateway script in Bash at `/home/user/app/gateway.sh`. Make sure it is executable. This script must:
    - **Request Validation**: Check the `HTTP_X_API_KEY` environment variable. If it does not exactly equal `SecretMigrate99`, print `Status: 403 Forbidden\n\nAccess Denied` and exit.
    - **Rate Limiting**: Check the `REMOTE_ADDR` environment variable. Use the directory `/tmp/rate_limit/` (create it if it doesn't exist) to track IP addresses. If a request from the same IP address is received less than 2 seconds after the previous request, print `Status: 429 Too Many Requests\n\nRate Limited` and exit.
    - **Execution**: If the request passes validation and rate limiting, the Bash script should execute the Python 3 script using the virtual environment (`/home/user/venv/bin/python /home/user/app/process.py`) and pass its standard output to the caller.

Ensure the final system is robust. `gateway.sh` will be tested via simulated CGI environment variables.