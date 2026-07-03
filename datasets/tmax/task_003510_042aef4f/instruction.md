We are migrating a legacy system from Python 2 to Python 3. The old application relied on a C library to parse a proprietary binary protocol using `ctypes`. However, the C library is plagued by memory safety issues and undefined behavior when handling malformed data. We want to rewrite the parsing logic safely in Rust and call it from a new Python 3 script.

Your objectives:
1. Create a Rust file at `/home/user/src/parser.rs`. It must export a C-ABI function with the following signature (conceptually in C):
   `int32_t parse_protocol(const uint8_t* input, size_t input_len, char* out_json, size_t out_max_len)`
   
   The function should parse the binary `input` using a strict state machine, serialize the extracted records to a JSON string, and copy the null-terminated JSON string into `out_json` (up to `out_max_len` bytes). 
   
   Protocol format (TLV):
   - 1-byte Type: `1` for ASCII String, `2` for Int32 (Little-Endian).
   - 1-byte Length: The size of the Value in bytes.
   - N-byte Value: The data.
   
   If parsing succeeds, return `0`. If the data is truncated, the type is unknown, or the state machine encounters any invalid state, return `-1` and do not modify `out_json`.
   
   The serialized JSON must be a single array of objects, strictly formatted without extra spaces (e.g., `[{"type":1,"value":"hello"},{"type":2,"value":42}]`).

2. Compile your Rust code to a shared library at `/home/user/libparser.so`. Use standard tools available (e.g., `rustc --crate-type=cdylib`). You may use the standard library, but no external crates (no `serde`, just build the JSON string manually to keep it simple).

3. Write a Python 3 script at `/home/user/app.py` that:
   - Loads `/home/user/libparser.so` using `ctypes`.
   - Reads the binary file located at `/home/user/data.bin`.
   - Allocates a 1024-byte buffer for the output JSON.
   - Calls `parse_protocol`.
   - Writes the resulting JSON string directly to `/home/user/output.json`.

Ensure your Python 3 script handles string decoding correctly and accurately passes the buffer sizes. Execute your Python script to produce the final `output.json`.