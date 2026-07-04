You are tasked with fixing a broken polyglot API server located at `/home/user/polyglot-service`. 

The project consists of a Rust-based HTTP server that delegates routing and data processing to a C library via FFI. Currently, the project fails to compile, and the C data processing logic contains bugs in its parameter parsing.

Your objectives:
1. **Fix the C Build System**: The `Makefile` in `/home/user/polyglot-service/c_src/` is incomplete and fails to build the required static library (`libapi_processor.a`). Fix it so that it correctly compiles `processor.c` and archives it into `libapi_processor.a`.
2. **Fix the C Implementation and FFI**: 
   - The Rust server expects a C function with the signature: 
     `void process_request(const char* method, const char* path, const char* query, char* response_buffer);`
   - The files `c_src/processor.c` and `c_src/processor.h` have a mismatching signature and memory bugs.
   - Update `processor.c` to correctly parse the `query` string for REST API calls. The query will be in the format `op=<operation>&values=<comma_separated_integers>` (e.g., `op=sum&values=10,20,30`).
   - The supported operations are `sum` and `max`.
   - The C function must write a valid JSON response into `response_buffer` (e.g., `{"result": 60}`). If the operation is unknown or parsing fails, write `{"error": "invalid"}`.
3. **Compile the Polyglot Project**: Navigate to `/home/user/polyglot-service` and run `cargo build`. Ensure it compiles successfully.
4. **Test the REST API**:
   - Start the compiled Rust server in the background (`./target/debug/polyglot-service &`). It will bind to `127.0.0.1:8080`.
   - Use `curl` to test the API and write the exact output to `/home/user/results.log`.
   - Make two requests:
     1. `curl -s "http://127.0.0.1:8080/api/process?op=sum&values=5,15,25"`
     2. `curl -s "http://127.0.0.1:8080/api/process?op=max&values=7,42,19"`
   - Each response should be on a new line in `/home/user/results.log`.

Ensure your C code safely parses the strings without buffer overflows. The `response_buffer` allocated by Rust is 256 bytes long.