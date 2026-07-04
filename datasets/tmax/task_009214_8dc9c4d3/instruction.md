As a QA engineer, I am setting up a new test environment for our sensor data pipeline. We have a legacy C library that computes a proprietary checksum for sensor readings using a specific numerical algorithm. 

Currently, the C project's `Makefile` is broken and fails to build the required shared library due to compilation and linking errors. I need you to fix the Makefile, build the shared library, and then write a data processing script in the language of your choice to process a batch of incoming test requests.

Here is the setup in `/home/user/sensor_sim`:
1. `sensor_calc.c`: The C source file containing `int compute_sensor_checksum(double value);`
2. `Makefile`: A broken makefile that is supposed to build `libsensor.so`.
3. `requests.jsonl`: A file containing incoming sensor data requests.

Your task:
1. **Fix the Makefile:** Modify `/home/user/sensor_sim/Makefile` so that running `make` successfully compiles `sensor_calc.c` into a shared library named `libsensor.so`. The C code uses functions from the math library, and it must be compiled as position-independent code for a shared library.
2. **Write a Processing Script:** Write a script in `/home/user/sensor_sim/process.sh` (or any script file you create and execute, like `process.py` or `process.rb`) that does the following:
   - Reads `/home/user/sensor_sim/requests.jsonl` line by line.
   - **Validates the request:** A request is valid ONLY if the JSON object has `"status": "active"` and the `"value"` is a number strictly greater than `0`.
   - **Cross-language interop (FFI):** For valid requests, load `libsensor.so` and pass the `"value"` to the `compute_sensor_checksum` C function.
   - **Output:** Write the results to `/home/user/sensor_sim/processed_outputs.jsonl`. Each line must be a JSON object.
     - If the request was valid, write: `{"id": <id>, "checksum": <computed_integer>}`
     - If the request was invalid, write: `{"id": <id>, "error": "invalid_request"}`

Ensure your script processes all lines in the exact order they appear in the input file. Output the final `processed_outputs.jsonl` exactly as specified.