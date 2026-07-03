You are an engineer setting up the foundation for a highly performant, polyglot microservice architecture. We need to create a C-based CGI executable that serves Protobuf-encoded data acting as a REST-like API endpoint.

Your task is to set up a small build system and write the necessary code in `/home/user/polybuild` (you will need to create this directory).

Perform the following steps:

1. **Protobuf Definition**: Create a file named `catalog.proto` defining a Protobuf message named `Product`. It must have three fields:
   - `id` (int32, field number 1)
   - `slug` (string, field number 2)
   - `in_stock` (bool, field number 3)

2. **C Implementation**: Write a C program named `api_endpoint.c`. This program must:
   - Include the generated Protobuf-C header for `catalog.proto`.
   - Create a `Product` message instance and populate it with `id = 101`, `slug = "mechanical-keyboard"`, and `in_stock = true`.
   - Serialize the message.
   - Print a valid HTTP response to `stdout`. The response must include exactly one HTTP header: `Content-Type: application/x-protobuf`, followed by a blank line (CRLF), followed immediately by the raw serialized binary Protobuf payload.

3. **Build System**: Create a `Makefile` in the same directory. The `Makefile` must have a default target `all` that:
   - Uses `protoc-c` to generate the C source and header files from `catalog.proto`.
   - Compiles `api_endpoint.c` and the generated Protobuf C source into an executable named `api_endpoint`. Ensure you link the `protobuf-c` library.

4. **Execution and Output**:
   - Run `make` to build the executable.
   - Run `./api_endpoint` and redirect its standard output to a file named `response.bin`.

Do not use any external web server frameworks; just output the raw HTTP format to stdout as described. Ensure you have the correct syntax for `protobuf-c` (e.g., initialization macros).