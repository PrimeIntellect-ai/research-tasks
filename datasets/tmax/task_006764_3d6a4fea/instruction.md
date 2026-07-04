You are tasked with building a local web service that organizes project files based on dynamically evaluated mathematical expressions. You will need to compile a provided C library for expression evaluation, write a Python web server that uses this library via `ctypes`, and handle specific HTTP routing.

**Initial State:**
You have a workspace at `/home/user/workspace`.
Inside, there is a C source file `/home/user/workspace/expr.c` and a header `/home/user/workspace/expr.h`. 
There is also a directory `/home/user/workspace/inbox/` containing several files named `dataset_1.dat`, `dataset_2.dat`, ... up to `dataset_10.dat`.

**Requirements:**

1. **Shared Library Compilation:**
   Compile `/home/user/workspace/expr.c` into a shared library named `/home/user/workspace/libexpr.so`. 

2. **Python Web Server & ABI Management:**
   Write a Python web server at `/home/user/workspace/server.py` using only the Python standard library (e.g., `http.server`). 
   The server must listen on `127.0.0.1` port `8080`.
   Load `libexpr.so` using `ctypes`. The C library exposes the following function:
   `int evaluate_math(const char* expression, int* out_result);`
   (Returns 0 on success, -1 on error. `out_result` holds the integer result of the evaluated expression).

3. **URL Routing and Logic:**
   The server must handle `GET` requests to the route `/organize`.
   It should accept three URL query parameters:
   - `prefix` (e.g., `dataset_`)
   - `expr` (a mathematical expression like `2+3` or `10-2`)
   - `dest` (a destination folder name)
   
   *Example Request:*
   `GET /organize?prefix=dataset_&expr=4%2B1&dest=archive`
   
   *When this endpoint is hit, the server must:*
   a. Extract the parameters.
   b. Pass the `expr` string to the `evaluate_math` C function.
   c. Retrieve the integer result (e.g., `5`).
   d. Construct the target filename by concatenating the prefix, the result, and `.dat` (e.g., `dataset_5.dat`).
   e. Move this file from `/home/user/workspace/inbox/` to `/home/user/workspace/organized/<dest>/`. Create the destination directory if it doesn't exist.
   f. Return an HTTP 200 response with the exact JSON body: 
      `{"status": "success", "file": "dataset_5.dat", "destination": "archive"}`

4. **Execution:**
   Run your Python server in the background. Once the server is up and listening on port 8080, write the exact word `READY` to `/home/user/workspace/status.txt` to indicate that automated testing can begin. Do not write anything else to this file.