I have a legacy Python 2 REST API application that wraps a custom C library for high-performance string processing. We need to migrate this entire application to Python 3 and ensure the API is fully operational.

There are three major issues you need to resolve:
1. **Vendored Package Fix:** The custom C library is located in `/app/vendored/libstrproc-1.0.2`. It has a known memory safety issue (undefined behavior) that triggers a segmentation fault when processing strings longer than 255 characters. You need to debug and fix the C code, then recompile it.
2. **Python 2 to 3 Migration:** The Python REST API in `/app/api/server.py` and its C-bindings wrapper in `/app/api/wrapper.py` are written in Python 2. You must migrate them to Python 3. Pay special attention to string/bytes conversions which have changed between Python 2 and 3.
3. **API Bring-up & Testing:** The API must run as a REST service listening on `127.0.0.1:8080`. It needs to provide an endpoint `POST /process` that accepts a JSON payload `{"input": "<string>"}` and returns `{"result": "<processed_string>"}`. 
Finally, write a bash script at `/app/test_e2e.sh` that sends 3 requests to the running API using `curl` (including one with a string longer than 255 characters) and saves the HTTP status codes to `/app/test_results.log`.

Please fix the C library, migrate the Python code, start the REST API as a background process, and ensure your `test_e2e.sh` script executes successfully. Leave the API running on port 8080.