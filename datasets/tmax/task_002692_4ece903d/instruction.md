You are an integration developer testing a new API endpoint that provides mathematical coordinate data. The API is known to sometimes corrupt data in transit, so the payload includes an error-correcting checksum.

You have been provided with a workspace at `/home/user/workspace` containing the following files:
1. `api_server.py`: A simple Python HTTP server that serves the corrupted mock data on port 8080.
2. `decoder.c`: A C library that implements a custom error-correcting algorithm. It exposes a function `void decode_payload(const char* input, char* output)` which takes a 5-character string, corrects any single-character error, and writes the 4-character corrected data to `output`.
3. `sorter.cpp`: A C++ program that reads lines of 4-character numbers from standard input, calculates their integer value, sorts them in descending order, and prints them to standard output.
4. `expected_output.txt`: The canonical, correctly sorted data that the API should ideally produce.

Your task:
1. **Polyglot Build**: 
   - Compile `decoder.c` into a shared library named `libdecoder.so`.
   - Compile `sorter.cpp` into an executable named `sorter`.
2. **API Testing**:
   - Start the `api_server.py` in the background (it binds to `127.0.0.1:8080`).
   - Write a Python script named `/home/user/workspace/integration_test.py` that:
     - Fetches the JSON response from `http://127.0.0.1:8080/data`. The response format is `{"payloads": ["string1", "string2", ...]}`.
     - Uses the `ctypes` module to load `libdecoder.so` and pass each string to `decode_payload` to retrieve the corrected 4-character string.
     - Pipes the corrected strings (newline-separated) into the `sorter` executable.
     - Captures the standard output of the `sorter`.
3. **Diffing and Validation**:
   - Compare the output of the `sorter` with the contents of `/home/user/workspace/expected_output.txt`.
   - Use the `diff` command (or Python equivalent) to find the differences.
   - If there are no differences, write the exact string `PASS` to `/home/user/workspace/test_result.log`. If there are differences, write the diff output to `/home/user/workspace/test_result.log`.

Do not modify the provided C/C++ files or the API server. Produce exactly the `/home/user/workspace/test_result.log` as your final output.