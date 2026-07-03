I am migrating an old Python 2 system to Python 3. As part of this, I'm rewriting the test suite for our core C library (`libprotorest.so`) into a native C test suite using CMake. This C library acts as a bridge: it takes raw binary protobuf payloads and encodes them into Base64 within a REST-compliant JSON payload.

However, I'm stuck on a few issues:
1. **Linker Error:** My `CMakeLists.txt` builds the shared library successfully, but the test executable `test_encoder` fails to link against `libprotorest.so` at link time. 
2. **Encoding Bug:** Our system has a Base64 encoding bug in the C library. It properly encodes the characters but fails to add the necessary `=` padding at the end of the string when the input length is not a multiple of 3. This is causing our REST API to reject the payloads.
3. **Missing Test:** I need you to add a test case to the test suite to ensure the bug stays fixed.

Here is what you need to do:
1. Navigate to `/home/user/project/`.
2. Fix the `CMakeLists.txt` so that the `test_encoder` target successfully links against the `protorest` shared library.
3. Fix the Base64 padding bug in `/home/user/project/src/encoder.c`. The `base64_encode` function should correctly append `=` or `==` padding characters to the output string.
4. In `/home/user/project/tests/test_encoder.c`, add a test function named `test_rest_payload` (and call it from `main`). It must use the library function `generate_rest_payload` with the input string `"Migrating to Py3"` (length 16). Assert that the exact returned JSON string is `{"payload": "TWlncmF0aW5nIHRvIFB5Mw=="}`.
5. Build the project in the `/home/user/project/build/` directory using CMake and Make.
6. Run the test executable. If it passes, create a file at `/home/user/test_result.log` with the exact contents `SUCCESS`.

All files currently exist in `/home/user/project/`. You must modify the code, verify the build, and run the test.