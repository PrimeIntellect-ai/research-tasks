You are helping a web developer fix a backend data processing pipeline. The pipeline uses a custom Rust-based log parsing tool that links against a C shared library. Currently, the project fails to compile due to a Makefile linking error in the C code and some Rust borrow checker errors. Additionally, the state machine logic for parsing the custom format is slightly broken.

Your tasks are:

1. **Fix the C shared library:**
   Navigate to `/home/user/pipeline/c_src`. The `Makefile` there is supposed to build a shared library `libfilter.so` from `filter.c`. However, it fails to build a proper shared library because it is missing the correct compiler and linker flags for position-independent code and shared object creation. Fix the Makefile and compile `libfilter.so`.

2. **Fix the Rust parser:**
   Navigate to `/home/user/pipeline/rust_src`. The Rust application parses a custom event log format, using FFI to call `is_valid_event` from `libfilter.so`. 
   Currently, `src/main.rs` fails to compile due to a borrow checker error (attempting to store references to local variables that get dropped). 
   Fix the Rust code so it compiles. You will likely need to change a reference type to an owned `String` in the `Event` struct and adjust the parsing logic.

3. **Run the parser:**
   The parser uses a simple state machine. The log format is:
   ```
   BEGIN <code>
   DATA <string>
   END
   ```
   For each event, if the C FFI function `is_valid_event(code)` returns true (1), the event should be added to the final list.
   Once the Rust code compiles, run it with the input file `/home/user/input.log` and specify the output file as `/home/user/output.json`.
   The command takes two arguments: `cargo run -- /home/user/input.log /home/user/output.json`
   (Make sure the `LD_LIBRARY_PATH` is set so the Rust program can find `libfilter.so` in `/home/user/pipeline/c_src`).

The final output must be a valid JSON array of objects, e.g., `[{"code": 200, "data": "success"}, ...]`, written to `/home/user/output.json`.