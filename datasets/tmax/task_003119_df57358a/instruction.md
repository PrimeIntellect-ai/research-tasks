I'm a systems programmer working on a data processing microservice, but I'm running into a C library linking issue and need help getting the full stack running. 

My application stack consists of:
1. A C shared library (`libprocessor.so`) that performs fast arithmetic.
2. A Python C-extension (`pyprocessor`) that wraps this library.
3. A Python web server (`app.py`) that implements a state-machine parser, uses the C-extension to process values, and exposes a REST endpoint.
4. An Nginx reverse proxy to route external traffic to the Python app.

Currently, the setup is broken in a few ways. All files are located in `/home/user/app/`.

Here is what you need to do:
1. **Fix the Build System & Linking**: The `setup.py` file fails to compile or link the `pyprocessor` extension properly. The C library `libprocessor.so` has already been built and is located in `/home/user/app/lib/`. You must modify `/home/user/app/setup.py` so that it correctly specifies the library directory (`/home/user/app/lib`) and sets the runtime library directory (rpath) so the module can find `libprocessor.so` at runtime. Then, build the extension in-place (`python3 setup.py build_ext --inplace`).
2. **Fix the State Machine**: Inside `/home/user/app/app.py`, there is a function `parse_data(filepath)` that reads `/home/user/app/data.txt`. The data contains a sequence of commands. The state machine should start in the `IDLE` state. When it reads "START", it moves to the `RECORDING` state. In `RECORDING`, if it reads "VAL <number>", it should call the C-extension's `multiply_by_two(<number>)` and add the result to a running total. If it reads "STOP", it moves back to `IDLE` (ignoring subsequent VALs). Fix the broken logic in the `parse_data` function so it returns the correct total.
3. **Start the App**: Run `python3 /home/user/app/app.py` in the background. It listens on `127.0.0.1:9000`.
4. **Configure the Reverse Proxy**: Create a minimal Nginx configuration at `/home/user/app/nginx.conf` that listens on port `8080` (without requiring root/sudo) and proxies all requests to `http://127.0.0.1:9000`. Start Nginx using this config.
5. **Verify**: Use curl to trigger the processing by making a GET request to the proxy: `curl -s http://127.0.0.1:8080/process > /home/user/result.json`

Ensure the final parsed total is correctly saved in `/home/user/result.json` (it should just be a JSON object like `{"result": 42}`).