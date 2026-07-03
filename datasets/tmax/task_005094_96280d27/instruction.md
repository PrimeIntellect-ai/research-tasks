You are a systems programmer debugging a dynamic linking issue in a C project. You have been given a shared library `/home/user/project/libcalc.so` that was supposed to export a function named `calculate_expression`, but due to an assembly macro error during compilation, the symbol was mangled and exported under a different name containing the substring `_asm_calc_`. 

Your goal is to identify the actual exported symbol, verify its behavior using Python, and expose this functionality through a local web service behind a reverse proxy.

Perform the following steps:

1. **Symbol Analysis**: Write a Python script `/home/user/project/parser.py` that executes `nm -D /home/user/project/libcalc.so` and uses a state machine to parse the output line by line. It must locate the exact symbol name that contains `_asm_calc_`.

2. **C-to-Python Binding**: Write a Python script `/home/user/project/server.py` that uses the `ctypes` library to load `/home/user/project/libcalc.so` and binds to the discovered symbol. The C function signature is equivalent to `int (int a, int b)`. 

3. **Web Service**: In the same `server.py` script, start a basic Python HTTP server on `127.0.0.1:9000`. When a GET request is made to `/`, it should call the C function with the arguments `a=5` and `b=7`, and return the integer result as plain text. Run this server in the background.

4. **Reverse Proxy Configuration**: Configure Nginx to act as a reverse proxy. Create or modify the Nginx configuration so that listening on `127.0.0.1:8080` forwards all requests to your Python server at `127.0.0.1:9000`. Start or reload Nginx to apply the changes.

5. **Verification Output**: Create a JSON file at `/home/user/project/result.json` containing the following keys:
   - `"symbol_name"`: The exact mangled symbol name you extracted from the library.
   - `"computation_result"`: The integer result returned by calling the C function with 5 and 7.

Ensure the Nginx proxy is fully functional. An automated test will curl `http://127.0.0.1:8080/` to verify the reverse proxy and check the contents of `result.json`.