You are acting as a mobile build engineer maintaining our data processing pipelines. We have a Rust-based telemetry parsing tool at `/home/user/mobile_telemetry` that extracts metrics from raw binary dumps. However, the pipeline is currently broken in multiple ways.

Here is what you need to do to fix the pipeline:

1. **Fix Memory Safety in Legacy C Code**: 
   The Rust tool uses FFI to call a legacy C decompression function located at `/home/user/mobile_telemetry/src/legacy_decoder.c`. 
   Currently, the `decode_stream` function crashes with segmentation faults on certain malformed inputs due to an out-of-bounds read. The function processes an input byte array. Whenever it encounters the byte `0xFF` (a skip marker), it unconditionally advances the input pointer by 3 bytes without checking if 3 bytes actually remain in the input buffer. 
   Fix the C code so that if an `0xFF` is encountered and there are fewer than 3 bytes remaining (including the `0xFF` itself), the function safely stops processing and returns the number of bytes written so far, instead of reading out of bounds.

2. **Implement a State Machine Parser**:
   Once decoded, the telemetry data consists of a series of packets. You need to implement the `parse_telemetry` function in `/home/user/mobile_telemetry/src/main.rs`.
   The parser must use a strict state machine to process the decoded byte stream sequentially.
   Packet structure:
   - `Header`: 1 byte (Always `0xAA`. If you see something else, skip bytes until you find `0xAA`).
   - `Type`: 1 byte (Valid types are `1` for Battery, `2` for DeviceName).
   - `Length`: 1 byte (`L`).
   - `Payload`: `L` bytes.
   - `Checksum`: 1 byte. (The XOR sum of `Type`, `Length`, and all `Payload` bytes. Does not include `Header`).
   
   If the checksum is valid:
   - For Type 1 (Battery): The payload is a 32-bit Big-Endian unsigned integer. Store it as `{"type": "battery", "value": <int>}`.
   - For Type 2 (DeviceName): The payload is a UTF-8 string. Store it as `{"type": "device", "value": "<string>"}`.
   
   Write the final parsed valid packets as a JSON array to `/home/user/parsed_metrics.json`.

3. **Cross-Compilation Configuration**:
   The parsing tool must be compilable for our mobile target pipeline.
   - Ensure the project successfully builds for the `aarch64-unknown-linux-gnu` target.
   - Implement conditional compilation in `main.rs`: Write a function `pub fn get_pipeline_arch() -> &'static str` that returns `"aarch64"` when compiled for the `aarch64` architecture, and `"x86_64"` when compiled for `x86_64`.

4. **Execution**:
   - Compile and run the project natively to read the raw binary file at `/home/user/telemetry.bin`.
   - Output the valid metrics to `/home/user/parsed_metrics.json`.
   - Do not use any external crates other than `serde` and `serde_json` (which are already in the `Cargo.toml`). `libc` and `cc` are provided for the FFI build.

Fix the code, build it, run it, and verify that both the cross-compilation check and the JSON output are correct.