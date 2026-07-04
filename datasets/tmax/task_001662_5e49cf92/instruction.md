You are a developer tasked with cleaning up a disorganized project, compiling a C extension, benchmarking it against a Python equivalent, and exposing the results via a reverse proxy.

Your workspace is located at `/home/user/project`. Inside, you will find several unorganized files.

Perform the following tasks:

1. **File Organization:**
   - Create the following directory structure inside `/home/user/project`: `C_src/`, `Python_src/`, `build/`, and `config/`.
   - Move `prime_c.c` to `C_src/`.
   - Move `prime_py.py` to `Python_src/`.

2. **C Compilation (FFI Prep):**
   - Compile `C_src/prime_c.c` into a shared library named `libprime.so` and place it in the `build/` directory. Use GCC and ensure it is compiled as position-independent code (PIC).

3. **Benchmarking via FFI:**
   - Write a new Python script at `/home/user/project/Python_src/benchmark.py`.
   - This script must use `ctypes` to load `../build/libprime.so` and call its `count_primes(int n)` function.
   - It must also import the `count_primes` function from `prime_py.py`.
   - Benchmark both implementations by calling `count_primes(50000)` 5 times each. Calculate the average execution time for C and Python.
   - The script must write the results to `/home/user/project/build/report.txt` in exactly this format:
     ```
     C_avg: <float>
     Py_avg: <float>
     Speedup: <float>
     ```
     *(Where Speedup is Py_avg / C_avg)*
   - Run your benchmark script to generate the `report.txt` file.

4. **Web Server & Reverse Proxy:**
   - Start a background Python HTTP server on port 9000 serving ONLY the `/home/user/project/build` directory.
   - Create an HAProxy configuration file at `/home/user/project/config/haproxy.cfg`.
   - Configure HAProxy to run as a frontend listening on `127.0.0.1:8080` (HTTP), forwarding all traffic to a backend pointing to your Python HTTP server at `127.0.0.1:9000`.
   - Start HAProxy in the background using your configuration file.

Once you are done, an automated system will run `curl -s http://127.0.0.1:8080/report.txt` to verify your work.