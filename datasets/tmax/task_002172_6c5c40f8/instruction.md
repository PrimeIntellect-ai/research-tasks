You are an integration developer responsible for building a fast API request processor in Rust that interfaces with a legacy C library.

We have a legacy C data processing module in `/home/user/c_module`. Unfortunately, the `Makefile` is broken, and the library isn't compiling correctly as a shared object (`libprocessor.so`). 

Additionally, the product manager left an audio note in `/app/update.wav` containing the new required configuration parameters for the API protocol (specifically, the protocol version number and the required transformation offset).

Your tasks:
1. Listen to or transcribe `/app/update.wav` to retrieve the protocol version and the transformation offset.
2. Fix the `Makefile` in `/home/user/c_module` so it successfully compiles `libprocessor.so` with standard ABI compatibility.
3. Create a Rust project in `/home/user/api_handler`.
4. Write a Rust program that uses FFI to link against `libprocessor.so`. The Rust program must compile to a binary named `api_processor` located at `/home/user/api_handler/target/debug/api_processor`.
5. The Rust program must simulate a REST API endpoint processor. It should accept exactly one command-line argument: a JSON string.
6. If the JSON string has the format `{"endpoint": "/api/v<VERSION>/process", "payload": "<DATA>"}`, where `<VERSION>` is the version from the audio file, the program should call the C function `void process_data(char* data, int offset)` on the `<DATA>` string, using the offset from the audio file.
7. The program must then print exactly the resulting JSON: `{"status": "success", "result": "<MODIFIED_DATA>"}` to standard output.
8. If the endpoint does not match the version, or the JSON is invalid, print `{"status": "error"}`.

Ensure your Rust program handles the FFI boundary safely and links to the C shared library correctly. Your final executable will be tested against N=1000 random JSON payloads to ensure bit-exact equivalence with our reference implementation.