I am migrating an old Python 2 web security API to Python 3.10. The system relies on a custom C extension for fast token validation, but the build and the application currently fail.

The application is located in `/home/user/app`.

Please perform the following steps to complete the migration:

1. **Fix the C Extension Build:** 
   Navigate to `/home/user/app/ext`. The `validator.c` file was written for Python 2 and uses `Py_InitModule`. Update the module initialization code to be compatible with Python 3 (name the module `validator`). 
   Also, fix `/home/user/app/ext/Makefile` so that it includes the Python 3.10 headers instead of Python 2.7 headers. Compile the extension by running `make` and copy the resulting `validator.so` to `/home/user/app/validator.so`.

2. **Fix the Circular Dependency:**
   If you try to import the application logic by running `python3 /home/user/app/server.py`, you will encounter an `ImportError` caused by a circular dependency between `server.py` and `auth.py`. 
   Resolve this graph dependency issue by creating a `/home/user/app/config.py` file. Move the `RATE_LIMIT` constant from `server.py` into `config.py`, and update both `server.py` and `auth.py` to import `RATE_LIMIT` from `config.py` instead of each other. Do not change any other application logic.

3. **Verify the Fix:**
   Once the extension compiles and the circular import is resolved, execute `/home/user/app/test_runner.py`. This script simulates a REST API request validation flow. It will automatically write the execution results to `/home/user/migration_result.log`.

Ensure that the `/home/user/migration_result.log` file is successfully generated.