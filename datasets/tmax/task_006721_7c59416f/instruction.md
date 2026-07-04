I am building a Web Security utility to act as a WebSocket fuzzer. To maximize performance while generating malformed packets, I am porting the core frame-building engine to Rust and calling it from a Python wrapper script using `ctypes`. 

However, I've run into two issues:
1. My Rust code has an ownership and borrow checker bug that prevents it from compiling.
2. I haven't finished translating the Rust FFI data structure and function signatures into my Python script.

Here is the setup:

The Rust file is located at `/home/user/framing.rs`. It exports a C-compatible function `generate_frame_bytes`.
The Python script is located at `/home/user/fuzzer.py`. It is partially written.

Your task is to:
1. Fix the borrow checker bug in `/home/user/framing.rs` without changing the struct definition or the function signature of `generate_frame_bytes`.
2. Compile the Rust code into a shared library named `/home/user/libframing.so`. (You can compile it directly using `rustc --crate-type cdylib framing.rs -o libframing.so`).
3. Complete the Python script `/home/user/fuzzer.py` by:
   - Defining the custom `WsFrame` data structure using `ctypes` to perfectly match the Rust `#[repr(C)]` struct. Note that `usize` in Rust translates to `ctypes.c_size_t`.
   - Loading the `libframing.so` library.
   - Setting the correct `.argtypes` and `.restype` for the `generate_frame_bytes` function.
   - Creating an instance of the `WsFrame` struct with `fin=1`, `opcode=2` (binary frame), and using the payload `"TEST"` (encoded as ASCII bytes).
   - Calling the Rust function to get the generated frame bytes.
   - Extracting the raw bytes from the returned pointer based on the length populated by the Rust function.
   - Writing the hex-encoded string of those bytes (all lowercase, no spaces or prefixes) to a log file located at `/home/user/frame_output.hex`.

Do not change the fundamental logic of the WebSocket frame generation in the Rust code—just fix the compile error. Once you have finished the code, execute `/home/user/fuzzer.py` so that `/home/user/frame_output.hex` is created.