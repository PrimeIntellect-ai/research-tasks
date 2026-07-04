I am migrating a legacy data processing pipeline from Python 2 to Python 3. The pipeline relies on a custom C extension for fast text processing, but the extension fails to compile and run under Python 3 due to changes in the Python C API.

I have placed the legacy C extension code at `/home/user/pipeline/fast_counter.c` and a test Python script at `/home/user/pipeline/process.py`. 

Your task is to:
1. Modify `/home/user/pipeline/fast_counter.c` so that it is fully compatible with Python 3. You will need to update the module initialization mechanism and integer types to match the Python 3 C API.
2. Create a `/home/user/pipeline/setup.py` file to configure the build system for this C extension (the module should be named `word_counter`).
3. Create a Python 3 virtual environment at `/home/user/venv`, activate it, and install the `word_counter` package into it.
4. Run the test script `/home/user/pipeline/process.py` using the Python 3 executable from the virtual environment. 
5. The `process.py` script expects the module to work and will output a summary. Pipe the output of this script directly to `/home/user/pipeline/output.log`.

Do not modify `process.py`. Ensure that your C code correctly parses the arguments and returns a valid Python 3 long integer. The final verification will check the contents of `/home/user/pipeline/output.log`.