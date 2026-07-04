You are an integration developer responsible for ensuring that two different backend services (one written in C, one in C++) return consistent data through our Python API gateway.

The project is located in `/home/user/api_integration/`. 

Your goals are to:
1. **Compile the Polyglot Backends**: 
   - Compile `/home/user/api_integration/backend_c.c` into a shared library named `libbackend_c.so`.
   - Compile `/home/user/api_integration/backend_cpp.cpp` into a shared library named `libbackend_cpp.so`.
   Both should be compiled with position-independent code (`-fPIC`) to be loadable by Python's `ctypes`.

2. **Orchestrate the End-to-End Test**:
   Write a Python test script at `/home/user/api_integration/test_runner.py` that performs the following steps:
   - Starts the API server (`python3 api.py`) as a background process on port 5000 and waits until the server is ready to accept connections.
   - Makes an HTTP GET request to `http://127.0.0.1:5000/api/v1/data` (which uses the C backend).
   - Makes an HTTP GET request to `http://127.0.0.1:5000/api/v2/data` (which uses the C++ backend).
   - Both endpoints return a JSON array of user objects (each containing an `id`, `name`, and `role`), but the records are completely unsorted.
   - Parse the JSON responses and sort both arrays in ascending order based on the `id` field.
   - Save the sorted V1 data to `/home/user/api_integration/v1_sorted.json` and the sorted V2 data to `/home/user/api_integration/v2_sorted.json`. When saving, use an indent of 2 spaces.
   - Run a system bash command from within the Python script to diff the two JSON files: `diff -u v1_sorted.json v2_sorted.json`.
   - Redirect the standard output of the diff command to `/home/user/api_integration/diff_output.txt`.
   - Finally, cleanly terminate the background API server process.

3. **Execution**:
   Once written, run your test script so that all artifacts (`libbackend_c.so`, `libbackend_cpp.so`, `v1_sorted.json`, `v2_sorted.json`, and `diff_output.txt`) are generated. 

If successful, `diff_output.txt` should be completely empty (because the sorted arrays should be identical). Do not modify `api.py`, `backend_c.c`, or `backend_cpp.cpp`.