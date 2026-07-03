You are a systems programmer working on modernizing a legacy C-library build system. 

The security team mandates that library dependency linking follows a strict secure-resolution policy, which is currently implemented in a legacy, undocumented, stripped binary located at `/app/sec_linker_oracle`. 

Your goal is to deprecate this binary by reimplementing its exact logic as a modern Python REST API, along with a CLI client.

**Requirements:**

1. **Reverse Engineer the Oracle:**
   The binary `/app/sec_linker_oracle` accepts a single command-line argument: the absolute path to a JSON file containing a library dependency graph.
   The JSON file has the following schema:
   ```json
   {
     "libraries": {
       "libName": ["dep1", "dep2"],
       ...
     }
   }
   ```
   You must feed various JSON graphs to this binary to deduce its precise linking rules. Pay attention to how it handles valid dependency trees, how it breaks ties when multiple libraries could be linked next, and how it handles cyclic dependencies. The output format of your tool must exactly match the standard output (stdout) of this binary.

2. **Build the REST API:**
   Create a Python API server at `/home/user/linker_api.py` using Flask or FastAPI.
   - It must listen on `127.0.0.1:8000`.
   - It must expose a `POST /api/v1/resolve` endpoint.
   - The endpoint should accept the aforementioned JSON schema in the request body.
   - It should return a JSON response: `{"status": "success", "output": "<exact_string_output_from_oracle>"}` or `{"status": "error", "output": "<exact_error_string_from_oracle>"}`.

3. **Build the CLI Client:**
   Create a Python script at `/home/user/resolve_cli.py`.
   - It must accept exactly one command-line argument: the path to a JSON dependency file.
   - It must read the file, send it via HTTP POST to your local REST API (`127.0.0.1:8000/api/v1/resolve`).
   - It must print *only* the value of the `"output"` field from the API response to standard output. 

*Constraints:*
- You may install necessary Python packages using pip.
- Ensure your API server is designed to run continuously in the background while the CLI script is executed.
- The `resolve_cli.py` script's standard output must be bit-for-bit identical to the standard output of `/app/sec_linker_oracle` for any given valid or cyclic JSON dependency graph.