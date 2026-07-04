You are an backend web developer building a high-performance numerical feature for a new web service. 

Your team has decided to use a C backend for the heavy lifting and a Python HTTP server for the API. However, the current codebase is broken and incomplete.

Here is what you need to do:

1. **Extract Configuration**:
   You have been provided an image at `/app/config.png` containing the deployment configuration. Extract the text from this image (e.g., using `tesseract`) to find the required `PORT` and `AUTH_TOKEN`.

2. **Fix and Build the C Backend**:
   In `/home/user/c_backend`, there is a C source file `algo.c` and a `Makefile`. The C code implements a "Weighted Matrix Trace" algorithm, but it has a mathematical bug. 
   - Apply the patch file located at `/home/user/fix_algo.patch` to fix the bug in `algo.c`.
   - The `Makefile` is currently broken (it fails to compile the shared library `libalgo.so`). Fix the `Makefile` (ensure you use proper tabs and compiler flags for a shared library) and build `libalgo.so`.
   - The function signature in C is: `double weighted_trace(double* matrix, double* weights, int size);`

3. **Build the Web Service**:
   Create a Python web server script at `/home/user/server.py` (you may use `Flask`, `FastAPI`, or standard library `http.server`).
   - The server must listen on `127.0.0.1` and the port extracted from `/app/config.png`.
   - It must require an `Authorization: Bearer <AUTH_TOKEN>` header for all requests, using the token extracted from the image. If the token is missing or incorrect, return a 401 Unauthorized status.
   - Implement a `POST /process` endpoint that accepts a JSON payload with the following custom structure:
     ```json
     {
       "size": N,
       "weights": [w_1, w_2, ..., w_N],
       "matrix": [
         [m_11, m_12, ..., m_1N],
         ...
         [m_N1, m_N2, ..., m_NN]
       ]
     }
     ```
   - The server should parse this JSON, use `ctypes` to call the `weighted_trace` function from `libalgo.so` (passing the flattened matrix, weights, and size), and return the result in the following JSON format:
     ```json
     {
       "result": <float>
     }
     ```

4. **Run the Service**:
   Once implemented, start your server in the background and write its process ID to `/home/user/server.pid`. Ensure it is fully running and listening for requests.