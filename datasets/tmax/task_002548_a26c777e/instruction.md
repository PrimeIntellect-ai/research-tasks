You are tasked with fixing a broken Python testing pipeline for a C library wrapper, acting as a systems programmer. 

In `/home/user/project`, there is a Python module `data_client.py` that uses `ctypes` to load a pre-compiled C library `/home/user/project/libdata.so`. Currently, the tests in `/home/user/project/test_client.py` fail immediately with an `OSError: libbackend.so: cannot open shared object file` because `libdata.so` was linked against a missing shared library `libbackend.so`.

Your objectives are:
1. **Fix the Linking Issue:** You cannot modify `libdata.so` directly. You must create a dummy C file `/home/user/project/libbackend.c`, compile it into `libbackend.so`, and figure out a way (e.g., modifying test runner scripts or configuring the environment) so that Python's `ctypes` can successfully load `libdata.so`. The dummy library must export a single function `void backend_init() {}`.
2. **Implement an Emulator:** `libdata.so` attempts to connect to a backend service via TCP on `127.0.0.1:8888`. Write a Python script `/home/user/project/emulator.py` that acts as this backend. It must accept a connection, read a custom binary serialized payload, and respond.
   - **Serialization Format:** Requests consist of a 2-byte unsigned integer (Big Endian) representing the payload length `L`, followed by `L` bytes of UTF-8 text. 
   - **Emulator Logic:** The emulator should read the request, reverse the UTF-8 text string, and send it back using the exact same serialization format. It should handle one request and then close the connection.
3. **Write Test Fixtures:** Modify `/home/user/project/test_client.py` to use `pytest`. Create a fixture named `emulator_service` that spawns `emulator.py` as a background subprocess before the test runs, and terminates it after the test completes. 
4. **Complete the Test:** In `test_client.py`, write a test `test_data_processing` that uses the `data_client` to send the string `"SystemsEngineering"` to the emulator, and asserts that the response deserialized from the client is `"gnireenignEsmetsyS"`.

To verify your work, ensure you run your tests and output the results in JSON format using pytest-json-report or a similar tool. Generate the final test output at `/home/user/project/test_report.json`.