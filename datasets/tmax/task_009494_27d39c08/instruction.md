You are a systems programmer tasked with debugging a C library linking issue and using the library to extract and process firmware data.

You have a partial Rust project located at `/home/user/firmware_decoder`. The project is intended to interface with a proprietary C library located at `/home/user/legacy/libfirmware.so`.

However, the Rust project currently fails to build and link. Your first task is to diagnose the linking issue. The C library expects the host application to provide a logging callback, and the Rust build system isn't properly configured to find and link the `.so` file.

Once you fix the linking and build issues, you must implement the main logic in the Rust project (`/home/user/firmware_decoder/src/main.rs`):

1. **FFI Interaction:**
   The C library exposes a function to retrieve an encoded firmware payload. You need to inspect the library (e.g., using standard Linux binary analysis tools) to find the exact symbol name for the retrieval function. Its C signature is known to be:
   `size_t get_firmware_blob(unsigned char* out_buffer, size_t max_len);`
   You must call this function to retrieve the data. A buffer of 1024 bytes is sufficient.

2. **Structured Data Parsing (TLV):**
   The returned data is in a custom TLV (Type-Length-Value) format. You must parse this binary structure:
   - **Type** (1 byte)
   - **Length** (2 bytes, little-endian)
   - **Value** (`Length` bytes)
   Read through the TLV records sequentially until you find the record with **Type = `0x02`** (which represents the executable bytecode payload). Ignore all other records.

3. **Emulator Implementation:**
   The payload inside the `0x02` record is custom bytecode for an 8-bit accumulator-based virtual machine. You must implement a minimal emulator in Rust to execute this bytecode and recover the hidden message.
   
   **VM Architecture:**
   - Single 8-bit Accumulator register (`ACC`), initialized to `0x00`.
   - An output byte stream (initially empty).
   
   **Instruction Set:**
   - `0x10 <val>` : LOAD - Set `ACC` to the literal 8-bit `<val>`.
   - `0x11 <val>` : ADD  - Add `<val>` to `ACC` (wrapping around on overflow).
   - `0x12 <val>` : XOR  - Bitwise XOR `ACC` with `<val>`.
   - `0x20`       : OUT  - Append the current value of `ACC` to the output byte stream.
   - `0xFF`       : HALT - Stop execution.

4. **Character Encoding & Output:**
   After the VM halts, the output byte stream will contain a valid UTF-8 string. 
   Write this exact decoded string to `/home/user/decoded_message.txt`.

**Constraints:**
- Do not modify the C library in `/home/user/legacy/`.
- The Rust project must compile cleanly with `cargo build`.
- You must correctly export any symbols expected by `libfirmware.so` from your Rust code.