I am migrating a legacy data processing pipeline from Python 2 to Python 3. The old pipeline relied on a brittle C extension to decode binary data. I want to replace the C extension with a safe, modern Rust library and call it from Python 3 using `ctypes`.

Here is what you need to do:

1. **Create a Rust FFI Library:**
   - Initialize a new Rust library project at `/home/user/decoder`.
   - Configure it to compile as a C dynamic library (`cdylib`).
   - Implement a function with the following C signature: 
     `isize decode_payload(const uint8_t* input, size_t input_len, uint8_t* output, size_t max_len);`
   - **Encoding Logic:** The input binary data is obfuscated. To decode it, you must perform a bitwise XOR on every byte with the value `0xAA`. 
   - After XORing, the resulting bytes must be validated as a legitimate UTF-8 string. 
   - If the decoded bytes are valid UTF-8 and fit within `max_len`, write them to the `output` buffer and return the length of the string (in bytes). If the bytes are invalid UTF-8 or exceed `max_len`, return `-1`.
   - Build the project in release mode.

2. **Create the Python 3 Script:**
   - Write a new Python 3 script at `/home/user/app/process.py`.
   - It should use the `ctypes` module to load your compiled Rust dynamic library (`/home/user/decoder/target/release/libdecoder.so`).
   - The script must read the binary file located at `/home/user/app/encoded.dat`.
   - Call the `decode_payload` function, allocating a sufficiently large output buffer (e.g., 1024 bytes).
   - Read the resulting decoded string, and write it exactly as-is to `/home/user/app/decoded.txt`.

3. **Generate a Migration Patch:**
   - I have left the original Python 2 script at `/home/user/app/legacy_process.py`.
   - To document the migration for our version control system, generate a standard unified diff between `/home/user/app/legacy_process.py` (original) and your new `/home/user/app/process.py` (modified).
   - Save this unified diff to `/home/user/app/migration.patch`. 

Ensure all files are created exactly at the specified paths. You do not need to delete any files. Run your Python script to ensure `/home/user/app/decoded.txt` is successfully generated.