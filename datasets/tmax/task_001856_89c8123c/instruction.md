We are in the process of porting a legacy Linux telemetry processor to run inside a minimal container. The legacy system relies on a proprietary data processor, provided as a stripped binary at `/app/legacy_processor`. 

Recently, we discovered that this binary crashes with a segmentation fault when fed specially crafted serialized data containing circular references or excessively deep nesting (similar to how some Go modules fail on circular imports). 

To safely use this binary in the new minimal container, we need you to write a Python-based pre-processor and sanitizer that will act as a firewall. 

We started writing a memory-safe Rust extension using PyO3 to handle the deserialization of our custom Tag-Length-Value (TLV) format, located in `/app/tlv_parser/`. However, the developer left before finishing it, and it currently fails to compile due to Rust ownership and borrow checker errors.

Your tasks are as follows:
1. Fix the Rust ownership errors in `/app/tlv_parser/src/lib.rs` so that it successfully compiles as a Python module. You can build it using `maturin develop` (maturin is already installed in the Python virtual environment at `/opt/venv`).
2. Write a Python CLI tool at `/app/sanitizer.py` that takes a single file path as a command-line argument.
3. `/app/sanitizer.py` must use the fixed `tlv_parser` module to deserialize the file's contents.
4. The Python script must analyze the deserialized data structure to detect circular references or any nesting deeper than 10 levels. 
5. If the file is perfectly valid, clean, and safe, the script must exit with status code `0`.
6. If the file contains circular references, deep nesting, or malformed TLV data, the script must exit with status code `1` (rejecting the payload).
7. Ensure your Python code is robust. We highly recommend using `hypothesis` (property-based testing) to write local tests for your sanitizer before finalizing, as your script will be tested against a hidden adversarial corpus.

Note: The virtual environment is located at `/opt/venv`. Activate it before running `maturin` or running your script.